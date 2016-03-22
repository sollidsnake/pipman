#!/usr/bin/env python3

from pip2pkgbuild import Pip2Pkgbuild
from pkgbuild_generation import install_packages, parse_packages
import argparse
import docopt

"""pipman.

Generate PKGBUILD from pip packages.

Usage:
    pipman (-h|--help)
    pipman [--target-dir=DIR] <packages>...

Options:
    -h --help  Print the help message
    --target-dir=DIR  Directory where the PKGBUILD are created [default: "."]
"""

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    parser = argparse.ArgumentParser(description='Generate PKGBUILD ' +
            'from pip packages')

    parser.add_argument('packages', metavar='packages',
            type=str, nargs='+',
            help='Packages to be generated')

    parser.add_argument('--target-dir', dest='dir',
            help='Directory where the PKGBUILDs will ' +
            'be generated. The current directory is the default')

    args = parser.parse_args()

    packages = parser.parse_args().packages

    if packages:
        dir = args.dir
        if not dir:
            dir = '.'

        # pip = Pip2Pkgbuild(packages)
        # pip.generate_all(dir)
        # install_packages(dir, *[elt for elt in parse_packages(packages)])
