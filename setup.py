from setuptools import setup, find_packages

setup(name='pipman',
      version='0.5.0',
      description='Generate PKGBUILD from pip packages',
      url='https://github.com/sollidsnake/pipman',
      author='Jesse Nazario',
      author_email='jessenzr@gmail.com',
      license='GPL',
      keywords='archlinux pacman packaging',
      packages=find_packages(),

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
