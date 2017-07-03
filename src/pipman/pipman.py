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
    -q                             Search for packages in pip's repository
    -S                             Generate PKGBUILDs and call makepkg to install them

Positional:
    packages                       Packages to be generated

"""

from docopt import docopt


def generate(args, quiet=False):
    from pip2pkgbuild import Pip2Pkgbuild
    dir = args['--target-dir']
    if dir is False:
        dir = '.'

    packages = args['<packages>']

    Pip2Pkgbuild(packages, quiet=quiet).generate_all(dir)


def install(args, quiet=False):
    from pip2pkgbuild import Pip2Pkgbuild
    dir = args['--target-dir']
    if dir is False:
        dir = '.'

    packages = args['<packages>']

    Pip2Pkgbuild(packages, quiet=quiet).install_all(dir)


def search(args, quiet=False):
    from search import search
    search(args['<packages>'])


if __name__ == '__main__':
    args = docopt(__doc__)

    action = generate
    quiet = False

    if args['-S'] and args['-s']:
        action = search
    elif args['-S']:
        action = install

    if args['-q']:
        quiet = True

    action(args, quiet)
