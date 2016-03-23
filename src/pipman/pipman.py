#!/usr/bin/env python3

"""pipman.

Generate PKGBUILD from pip packages

Usage:
    pipman (-h | --help)
    pipman [options] <packages>...

Options:
    -h --help                      Show this screen.
    -t <dir>, --target-dir <dir>   target dir [default: .].

Positional:
    packages                       Packages to be generated

"""

from pkgbuild_generation import install_packages, parse_packages
import docopt


if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')
    print("{} : {}".format(PACKAGES, DIR_))
    for k, v in ARGS.items():
        print("{} : {}".format(k, v))


        # pip = Pip2Pkgbuild(packages)
        # pip.generate_all(dir)
        # install_packages(dir, *[elt for elt in parse_packages(packages)])
