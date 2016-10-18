#!/usr/bin/env python3

"""pipman.
Generate PKGBUILD from pip packages

Usage:
    pipman (-h | --help)
    pipman [options] <action> <packages>...

Options:
    -h --help                      Show this screen.
    -t <dir>, --target-dir <dir>   Target dir [default: .].
    -n --no-install                Only generate the pkgbuild, do not install the package

Positional:
    packages                       Packages to be generated

Action:
    install                        Install the package
    search                         Seach for the package

"""

from docopt import docopt


def generate(args):
    from pip2pkgbuild import Pip2Pkgbuild
    dir = args['--target-dir']
    if dir is False:
        dir = '.'

    packages = args['<packages>']

    Pip2Pkgbuild(packages).generate_all(dir)


def search(args):
    from search import search
    search(args['<packages>'])


if __name__ == '__main__':
    args = docopt(__doc__)

    action = args['<action>']
    action_index = {
        'search': search,
        'install': generate,
    }

    action_index[action](args)
