from setuptools import setup


setup(name='pipman',
      version='0.5.0',
      description='Generate PKGBUILD from pip packages',
      url='https://github.com/sollidsnake/pipman',
      author='Jesse Nazario',
      author_email='jessenzr@gmail.com',
      license='GPL',
      keywords='archlinux pacman packaging',
      packages=['log', 'misc', 'pip2pkgbuild', 'pipman']
)
