#!/usr/bin/env python3

"""pipman.
Generate PKGBUILD from pip packages

Usage:
    pipman (-h | --help)
    pipman [options] <packages>...
    pipman [options]

Examples:
    pipman sympy
    pipman numpy sym --target-dir=~/my-builds/
    pipman -S colorama
    pipamn -Su

Options:
    -h --help                     Show this screen.
    -t <dir>, --target-dir <dir>  Target dir [default: .].
    -q                            Search for packages in pip's repository
    -S                            Generate PKGBUILDs and call makepkg to install them
    -s                            Search for packages in pip's repository
    -u                            Update packages installed using pipman

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

def update(args=None, quite=False):
    from pip2pkgbuild import InstallData, Pip2Pkgbuild
    packages = InstallData().check_updates(quiet)

    from colorama import Fore, Style

    print()

    if not packages:
        print('there\'s nothing to do')
        return

    print('The following packages will be updated:')

    for package in packages:
        print("%s%s %s%s%s -> %s%s%s" % (
            Style.BRIGHT,
            package,
            Fore.RED,
            packages[package]['current'],
            Fore.RESET,
            Fore.GREEN,
            packages[package]['next'],
            Fore.RESET,
        ))

    print(Style.NORMAL + 'Do you wish to continue? [Y/n] ', end='')
    answer = input()

    if answer == 'n':
        return

    Pip2Pkgbuild(packages.keys(), quiet=quiet).install_all()


if __name__ == '__main__':
    args = docopt(__doc__)

    action = generate
    quiet = False

    if args['-S'] and args['-s']:
        action = search
    elif args['-S'] and args['-u']:
        action = update
    elif args['-S']:
        action = install

    if args['-q']:
        quiet = True

    action(args, quiet)
