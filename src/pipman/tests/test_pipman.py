import unittest
import os
import subprocess
import shutil

from pip2pkgbuild import Pip2Pkgbuild, InstallData
from misc import DEVNULL, PYTHON_VERSION


class TestPipman(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.package = 'click'
        self.package_name = 'python-click'
        self.dest = '/tmp/pipman-test'

        # remove dest directory
        shutil.rmtree(self.dest)

        self.out = self._generate()

    def _generate(self):
        Pip2Pkgbuild([self.package], quiet=True).generate_all(self.dest)

        working_dir = os.path.join(self.dest, self.package_name)
        return subprocess.call(['makepkg -sf'],
                               cwd=working_dir,
                               shell=True,
                               stdout=DEVNULL,
                               stderr=subprocess.STDOUT)

    def test_if_makepkg_command_finished_successfully(self):
        self.assertEqual(self.out, 0)

    def test_if_package_files_were_installed(self):
        init_file = os.path.join(self.dest, self.package_name, 'pkg',
                                 self.package_name, 'usr', 'lib',
                                 'python' + PYTHON_VERSION,
                                 'site-packages', self.package, '__init__.py')
        file_exists = os.path.isfile(init_file)

        self.assertEqual(file_exists, True)

    def test_config_file(self):
        InstallData.DATA_DIR = '/tmp/pipman-test/'

        try:
            os.remove('/tmp/pipman-test/data.json')
        except FileNotFoundError:
            pass

        data = InstallData()
        pack = Pip2Pkgbuild.compile_package_info(self.package)
        data.add_package(pack)
        data.save_to_file()

        data = InstallData()
        self.assertEqual(data.data, {
            "installedPackages":
            {pack['pkgname']: data._get_package_data(pack)}
        })
