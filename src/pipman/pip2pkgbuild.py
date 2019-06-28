import subprocess
import re
import os
import shutil
import venv

from misc import VENV_DIR, VENV_PIP, ENCODING, DEVNULL
from misc import blacklist
from log import Log
import json


class InstallData:
    DATA_DIR = os.path.join(
        os.path.expanduser('~'),
        '.local', 'share', 'pipman'
    )
    def __init__(self):
        """Loads packages into self.data"""

        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)

        self.data_file = os.path.join(self.DATA_DIR, 'data.json')

        try:
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}

        if not 'installedPackages' in self.data.keys():
            self.data['installedPackages'] = {}

    def add_package(self, pack):
        self.data['installedPackages'][pack['pkgname']] = self._get_package_data(pack)

    def remove_package(self, pack):
        self.data['installedPackages'].pop(pack, None)

    def save_to_file(self):
        try:
            with open(self.data_file, 'w') as f:
                f.write(json.dumps(self.data))
        except FileNotFoundError:
            self.data = {}

    def check_updates(self, quiet):
        update_candidates = {}
        uninstalled = []

        pip2pkg = Pip2Pkgbuild()
        pip2pkg._create_virtualenv()

        for pack in self.data['installedPackages'].items():
            pip2pkg.install_in_venv(pack[1]['name'])
            info = Pip2Pkgbuild.compile_package_info(pack[1]['name'])

            # check if package was uninstalled by pacman
            if not pip2pkg.is_package_installed(pack[0]):
                uninstalled.append(pack[0])
                continue

            if info['Version'] != pack[1]['version']:
                update_candidates[pack[1]['name']] = {
                    'current': pack[1]['version'],
                    'next': info['Version'],
                }

        # remove uninstalled packages
        for pack in uninstalled:
            self.remove_package(pack)

        self.save_to_file()

        return update_candidates

    @staticmethod
    def _get_package_data(pack):
        return {
            'version': pack['Version'],
            'name': pack['Name'],
        }

class Pip2Pkgbuild():

    log = Log()

    def __init__(self, packages=[], quiet=False):
        self.setup_packages(packages, quiet)

    def is_package_installed(self, package):
        try:
            self._exec(subprocess.check_call, ['pacman', '-Qi', package], True)
        except subprocess.CalledProcessError:
            return False

        return True

    def setup_packages(self, packages, quiet=False):
        # if quiet is True, hide all output
        self.set_quiet(quiet)

        # start virtualenv
        self._create_virtualenv()

        # intialize packages variable
        self.packages = {}
        self.dependencies = {}

        # install and create package dict
        for pack in packages:
            if pack in blacklist:
                continue

            self.install_in_venv(pack)
            self.packages[pack] = Pip2Pkgbuild.compile_package_info(pack)

    def _exec(self, func, command, quiet=None):
        if quiet is None:
            quiet = self.quiet

        if quiet:
            stdout = stderr = DEVNULL
            func(command, stdout=stdout, stderr=stderr)
            return

        func(command)

    def set_quiet(self, quiet):
        self.quiet = quiet

        if quiet:
            import logging
            self.log.set_level(logging.CRITICAL)

    def _create_virtualenv(self, force=False):
        """Create virtualenv to install packages"""
        Pip2Pkgbuild.log.info("Preparing virtualenv")

        if force:
            shutil.rmtree(VENV_DIR)

        if os.path.exists(VENV_DIR):
            return

        venv.create(VENV_DIR,
                    with_pip=True)

        # upgrade pip
        Pip2Pkgbuild.log.info('checking for pip upgrade')
        self._exec(subprocess.check_call, [VENV_PIP, 'install', '-U', 'pip'])

    def generate_all(self, prefix='.'):
        """Generate package/PKGBUILD for every package in self.packages"""

        # check if directories don't exist
        for pack in self.packages:
            pack = self.packages[pack]
            dir = os.path.join(prefix, pack['pkgname'])
            if os.path.exists(dir):
                Pip2Pkgbuild.log.error("Directory '%s' already exists" % dir)
                return

            # store directory in package dict
            self.packages[pack['pack']]['dir'] = dir

        for pack in self.dependencies:
            pack = self.dependencies[pack]
            dir = os.path.join(prefix, pack['pkgname'])
            if os.path.exists(dir):
                Pip2Pkgbuild.log.error("Directory '%s' already exists" % dir)
                return

            # store directory in package dict
            self.dependencies[pack['pack']]['dir'] = dir

        # generate the package build and store in package/PKGBUILD
        for pack in self.packages:
            pack = self.packages[pack]
            pkgbuild = Pip2Pkgbuild._generate_pkgbuild(pack)
            os.makedirs(pack['dir'])

            with open(os.path.join(pack['dir'], 'PKGBUILD'), 'w') as f:
                f.write(pkgbuild)

        for pack in self.dependencies:
            pack = self.dependencies[pack]
            pkgbuild = Pip2Pkgbuild._generate_pkgbuild(pack)
            os.makedirs(pack['dir'])

            with open(os.path.join(pack['dir'], 'PKGBUILD'), 'w') as f:
                f.write(pkgbuild)

    def install_all(self, prefix='.'):
        """Install the packages"""
        self.data = InstallData()

        self.generate_all(prefix)
        for _, dep in self.dependencies.items():
            path = os.getcwd()
            os.chdir(os.path.join(prefix, dep['pkgname']))
            self._exec(subprocess.check_call,
                       ['makepkg', '--install', '--asdeps'], quiet=False)
            os.chdir(path)
            self.data.add_package(dep)

        for _, pack in self.packages.items():
            path = os.getcwd()
            os.chdir(os.path.join(prefix, pack['pkgname']))
            self._exec(subprocess.check_call,
                       ['makepkg',
                        '--install',
                        os.path.join(prefix, pack['pkgname'])])
            os.chdir(path)
            self.data.add_package(pack)

        self.data.save_to_file()

    def install_in_venv(self, package):
        """Install package in virtualenv"""
        Pip2Pkgbuild.log.info("Installing '%s' in virtualenv" % package)

        # install package in virtualenv pip
        self._exec(subprocess.check_call,
                   [VENV_PIP, 'install',
                    '--disable-pip-version-check', package])

        dependencies = subprocess.check_output([VENV_PIP, 'show', package])
        dependencies = dependencies.decode(ENCODING)

        try:
            dependencies = re.search("Requires: (.*)$", dependencies)\
                             .group(1).split(', ')

            # add dependencies to self.packages, if not there yet
            for dep in dependencies:
                if dep and dep not in self.dependencies.keys():
                    self.dependencies[dep] = Pip2Pkgbuild.compile_package_info(dep)

        except AttributeError:
            dependencies = None

    @staticmethod
    def _generate_pkgbuild(package_info):
        """Generate PKGBUILD for package"""
        Pip2Pkgbuild.log.info("Generating pkgbuild for %s"
                              % package_info['pack'])

        # regex to match version and release
        version = package_info['Version']

        # store the pkgbuild output variable in 'lines' var
        lines = []

        lines.append('# PKGBUILD generated by pipman')
        lines.append('# Python package author: %s <%s>'
                     % (package_info['Author'], package_info['Author-email']))
        lines.append('pkgname=%s' % package_info['pkgname'])
        lines.append('pkgver=%s' % version)
        lines.append('pkgrel=1')

        lines.append('pkgdesc="%s"' % package_info['Summary'])
        lines.append('arch=(any)')
        lines.append('url="%s"' % package_info['Home-page'])
        lines.append('license=(%s)' % package_info['License'])
        lines.append('makedepends=("python" "python-pip")')

        lines.append('build() {')
        lines.append('  pip install --no-deps --target="%s" %s==%s'
                     % (package_info['pack'], package_info['pack'], version))
        lines.append('}')

        lines.append("package() {")
        lines.append('  sitepackages=$(python -c "import site; print(site.getsitepackages()[0])")')
        lines.append('  mkdir -p $pkgdir/"$sitepackages"')
        lines.append(('  cp -r $srcdir/%s/* ' +
                      '$pkgdir/"$sitepackages"')
                     % package_info['pack'])
        lines.append('}')

        return "\n".join(lines)

    @staticmethod
    def compile_package_info(package):
        """Store 'pip show package' in dict"""
        Pip2Pkgbuild.log.info("Checking package info")

        info = subprocess.check_output([VENV_PIP, 'show', package],
                                       stderr=DEVNULL)

        # we need to encode terminal output
        info = info.decode(ENCODING)

        # regex to match the values before and after :
        info = re.findall("^([\w-]+): (.*)$", info, re.MULTILINE)

        info_dict = {}

        for i in info:
            info_dict[i[0]] = i[1]

        info_dict['pack'] = package
        info_dict['pkgname'] = package.lower()
        if info_dict['pkgname'][:7] != "python-":
            info_dict['pkgname'] = "python-%s" % info_dict['pkgname']

        return info_dict
