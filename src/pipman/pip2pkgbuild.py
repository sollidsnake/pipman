import subprocess
import re
import os
import venv

from misc import VENV_DIR, VENV_PIP, ENCODING, DEVNULL
from misc import PYTHON_VERSION, blacklist
from log import Log


class Pip2Pkgbuild():

    log = Log()

    def __init__(self, packages):
        # start virtualenv
        self.__create_virtualenv__()

        # intialize packages variable
        self.packages = {}

        # install and create package dict
        for pack in packages:
            if pack in blacklist:
                continue

            self.install_in_venv(pack)
            self.packages[pack] = Pip2Pkgbuild.compile_package_info(pack)

    def __create_virtualenv__(self):
        """Create virtualenv to install packages"""
        Pip2Pkgbuild.log.info("Preparing virtualenv")

        if os.path.exists(VENV_DIR):
            return

        venv.create(VENV_DIR,
                with_pip=True)

        # upgrade pip
        Pip2Pkgbuild.log.info('checking for pip upgrade')
        subprocess.check_call([VENV_PIP,
            'install',
            '-U',
            'pip'])

    def generate_all(self, prefix='.'):
        """Generate package/PKGBUILD for every package in self.packages"""

        # check if directories don't exist
        for pack in self.packages:
            pack = self.packages[pack]
            dir = os.path.join(prefix, pack['pkgname'])
            if os.path.exists(dir):
                Pip2Pkgbuild.log.error("Directory '%s' already exists" % dir)
                quit()

            # store directory in package dict
            self.packages[pack['pack']]['dir'] = dir

        # generate the package build and store in package/PKGBUILD
        for pack in self.packages:
            pack = self.packages[pack]
            pkgbuild = Pip2Pkgbuild.__generate_pkgbuild__(pack)
            os.makedirs(pack['dir'])

            with open(os.path.join(pack['dir'], 'PKGBUILD'), 'w') as file_:
                file_.write(pkgbuild)

    def install_in_venv(self, package):
        """Install package in virtualenv"""
        Pip2Pkgbuild.log.info("Installing '%s' in virutalenv" % package)

        # install package in virtualenv pip
        subprocess.check_call([VENV_PIP,
                               'install',
                               '--disable-pip-version-check',
                               package])

        dependencies = subprocess.check_output([VENV_PIP, 'show', package])
        dependencies = dependencies.decode(ENCODING)

        try:
            dependencies = re.search("Requires: (.*)$", dependencies)\
                    .group(1).split(', ')

            # add dependencies to self.packages, if not there yet
            for dep in dependencies:
                if dep and dep not in self.packages.keys():
                    self.packages[dep] = Pip2Pkgbuild.compile_package_info(dep)

        except AttributeError:
            dependencies = None

    @staticmethod
    def __generate_pkgbuild__(package_info):
        """Generate PKGBUILD for package"""
        Pip2Pkgbuild.log.info("Generating pkgbuild for %s"
                              % package_info['pack'])

        # regex to match version and release
        ver_rel = re.search(r"(\d+(?:\.\d+)+)(?:-(\d+))?",
                            package_info['Version'])

        version = ver_rel.group(1)
        release = ver_rel.group(2)

        if not release:
            release = '1'

        # store the pkgbuild output variable in 'lines' var
        return open("PKGBUILD.tpl").read().format(
            aut=package_info['Author'],
            authmail=package_info['Author-email'],
            pkgname=package_info['pkgname'],
            pkgver=version,
            pkgrel=release,
            pkgdesc=package_info['Summary'],
            url=package_info['Home-page'],
            license=package_info['License'],
            depends=" ".join(['"' + e + '"' for e in package_info['Requires'].split(', ')]),
            pack=package_info['pack'],
            pyversion=PYTHON_VERSION
            )

    @staticmethod
    def compile_package_info(package):
        """Store 'pip show package' in dict"""
        Pip2Pkgbuild.log.info("Checking package info")

        info = subprocess.check_output([VENV_PIP, 'show', package],
                                       stderr=DEVNULL)

        # we need to encode terminal output
        info = info.decode(ENCODING)

        # regex to match the values before and after :
        info = re.findall(r"^([\w-]+): (.*)$", info, re.MULTILINE)

        info_dict = {}

        for i in info:
            info_dict[i[0]] = i[1]

        info_dict['pack'] = package
        info_dict['pkgname'] = "python-%s" % package.lower()

        return info_dict
