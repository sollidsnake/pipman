import subprocess
import re
from setuptools import setup

from src.pipman.misc import ENCODING

version_git = subprocess.check_output(["git", "describe"]).rstrip()
version_git = version_git.decode(ENCODING)

version_git = re.search("\d+\.\d+\.\d+",
                        version_git).group(0)

setup(name='pipman',
      version=version_git,
      description='Generate PKGBUILD from pip packages',
      url='https://github.com/sollidsnake/pipman',
      author='Jesse Nazario',
      author_email='jessenzr@gmail.com',
      license='GPL',
      keywords='archlinux pacman packaging',
      package_dir={'': 'src'},
      packages=['pipman', 'pipman.pip2', 'pipman.color', 'pipman.venv2'],

      classifiers=[

          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers'
          'Intended Audience :: System Administrators'

          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: GNU General Public License v3 ' +
          'or later (GPLv3+)',
      ]
)
