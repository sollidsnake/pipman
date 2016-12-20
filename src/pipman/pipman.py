#!/usr/bin/env python3

"""pipman.
Generate PKGBUILD from pip packages

Usage:
    pipman (-h | --help)
    pipman [options] <packages>...

Examples:
    pipman sympy
    pipman numpy sympy --target-dir=/tmp
    pipman -s browser
    pipman -i browser

Options:
    -h --help                      Show this screen.
    -t <dir>, --target-dir <dir>   Target dir [default: .].
    -s                             Search for packages in pip's repository
    -i                             Generate PKGBUILDs and call makepkg to install them

Positional:
    packages                       Packages to be generated

"""

from docopt import docopt


def generate(args):
    from pip2pkgbuild import Pip2Pkgbuild
    dir = args['--target-dir']
    if dir is False:
        dir = '.'

    packages = args['<packages>']

    Pip2Pkgbuild(packages).generate_all(dir)


def install(args):
    from pip2pkgbuild import Pip2Pkgbuild
    dir = args['--target-dir']
    if dir is False:
        dir = '.'

    packages = args['<packages>']

    Pip2Pkgbuild(packages).install_all(dir)


def search(args):
    from search import search
    search(args['<packages>'])


if __name__ == '__main__':
    args = docopt(__doc__)

    action = generate

    if args['-s']:
        action = search

    if args['-i']:
        action = install

    action(args)
