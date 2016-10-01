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
import os

from pkgbuild_generation import install_packages  # , parse_packages
from color import colorize, ForeGround
from search import search_and_print
from misc import VENV_DIR
from pacman import makepkg
from venv2 import Venv
from pip2 import PackageNotFound

import docopt


def signal_handler(signal_, _):
    """catch sigint and exit without stacktrace"""
    print('pipman aborted by signal %s' % signal_)
    sys.exit(1)

# TODO : find how install dependencie as dependencie (for pacman)
# TODO : put file in /tmp or clean after install (if not --no-install)


def init_user_log():
    """init user log"""
    log = logging.getLogger('user')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter(colorize("pipman: ",
                                   ForeGround.magenta) + "\t %(message)s"))
    log.addHandler(stream_handler)
    log.setLevel(logging.INFO)
    return log


def init_debug_log():
    """init debug log"""
    debug = logging.getLogger('debug')
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(
        logging.Formatter(">>> debug: %(message)s <<<"))
    debug.addHandler(stream_handler)
    debug.setLevel(logging.INFO)
    return debug


def install_if(pkgs, path, venv, no_install):
    pkgs_ = install_packages(path, *pkgs, venv=venv)

    if not no_install:
        for pkg in pkgs_:
            pkg_dir = os.path.join(path, pkg[1])
            makepkg(pkg_dir, install=not no_install)


if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    signal.signal(signal.SIGINT, signal_handler)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')
    ACT = ARGS['<action>']

    DEBUG, USER = init_debug_log(), init_user_log()

    DEBUG.info("Creating venv in %s", VENV_DIR)
    VENV = Venv(VENV_DIR)

    ACTIONS = {
        'search': lambda: search_and_print(PACKAGES),
        'install': lambda: install_if(PACKAGES, DIR_, VENV,
                                      ARGS.get('--no-install', False)),
        'generate': lambda: install_if(PACKAGES, DIR_, VENV, False)
    }

    DEBUG.info("List of packages : %s", PACKAGES)

    OUTPUT = ACTIONS[ACT]
    try:
        OUTPUT()
    except PackageNotFound as exc:
        USER.log(logging.WARNING, exc.pretty_print())
    except PermissionError as exc:
        USER.log(logging.ERROR, "Unable to write the PKGBUILD, Please make sure\
                 you have the right to write to %s", exc.filename)
