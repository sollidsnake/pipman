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

import logging
import sys
from pkgbuild_generation import install_packages, parse_packages
import docopt

if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')
    print("{} : {}".format(PACKAGES, DIR_))
    for k, v in ARGS.items():
        print("{} : {}".format(k, v))
    log = logging.getLogger("user")
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter("pipman: %(message)s"))
    log.addHandler(stream_handler)
    log.setLevel(logging.INFO)

    # pip = Pip2Pkgbuild(packages)
    # pip.generate_all(dir)
    log.info("List of packages : %s", PACKAGES)
    install_packages(DIR_, *PACKAGES)
