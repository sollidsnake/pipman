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

import logging
import sys
import signal
import shutil
import os

from pkgbuild_generation import install_packages, parse_packages
from color2 import *
from search import search_and_print
from misc import VENV_DIR
from pacman import makepkg

import docopt

def clean():
    """clean tmp files (usefull if venv not fully installed)"""
    shutil.rmtree(VENV_DIR)

def signal_handler(signal_, _):
    """catch sigint and exit without stacktrace"""
    print('pipman aborted by signal %s' % signal_)
    clean()
    sys.exit(1)

# TODO : find how install dependencie as dependencie (for pacman)
# TODO : put file in /tmp or clean after install (if not --no-install)

if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    signal.signal(signal.SIGINT, signal_handler)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')
    ACT = ARGS['<action>']

    log = logging.getLogger('user')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(colorize("pipman: ", ForeGround.magenta) + "\t %(message)s"))
    log.addHandler(stream_handler)
    log.setLevel(logging.INFO)

    debug = logging.getLogger('debug')
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter(">>> debug: %(message)s <<<"))
    debug.addHandler(stream_handler)
    debug.setLevel(logging.INFO)

    # TODO : pass option to the action function
    ACTIONS = {
        'install' : install_packages,
        'search' : lambda _, args, *p: search_and_print(list(p), args)
    }

    debug.info("List of packages : %s", PACKAGES)
    ACTIONS[ACT](DIR_, ARGS, *PACKAGES)
