#!/usr/bin/env python3

from pip2pkgbuild import Pip2Pkgbuild
import argparse

parser = argparse.ArgumentParser(description='Generate PKGBUILD ' +
                                 'from pip packages')

parser.add_argument('packages', metavar='packages',
                    type=str, nargs='+',
                    help='Packages to be generated')

parser.add_argument('--target-dir', dest='dir',
                    help='Directory where the PKGBUILDs will ' +
                    'be generated. The current directory is the default')

args = parser.parse_args()

packages = args.packages

if packages:
    dir = args.dir
    if not dir:
        dir = '.'

    pip = Pip2Pkgbuild(packages)
    pip.generate_all(dir)
