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
import signal

from pkgbuild_generation import install_packages, parse_packages
import docopt

def signal_handler(signal_, _):
    """catch sigint and exit without stacktrace"""
    print('pipman aborted by signal %s' % signal_)
    sys.exit(1)

if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    signal.signal(signal.SIGINT, signal_handler)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')

    log = logging.getLogger('user')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter("pipman: %(message)s"))
    log.addHandler(stream_handler)
    log.setLevel(logging.INFO)

    debug = logging.getLogger('debug')
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(">>> debug: %(message)s <<<"))
    debug.addHandler(stream_handler)
    debug.setLevel(logging.INFO)

    # pip = Pip2Pkgbuild(packages)
    # pip.generate_all(dir)
    log.info("List of packages : %s", PACKAGES)
    install_packages(DIR_, *PACKAGES)
