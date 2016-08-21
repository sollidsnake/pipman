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
        logging.Formatter(colorize("pipman: ", ForeGround.magenta) + "\t %(message)s"))
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

if __name__ == "__main__":
    ARGS = docopt.docopt(__doc__)

    signal.signal(signal.SIGINT, signal_handler)

    PACKAGES = ARGS['<packages>']
    DIR_ = ARGS.get('--target-dir', '.')
    ACT = ARGS['<action>']

    DEBUG, USER = init_debug_log(), init_debug_log()

    VENV = Venv(VENV_DIR)

    # TODO : pass option to the action function
    ACTIONS = {
        'install': install_packages,
        'search': lambda _, args, *p, **kw: search_and_print(list(p), args, **kw)
    }

    DEBUG.info("List of packages : %s", PACKAGES)
    OUTPUT = ACTIONS[ACT](DIR_, ARGS, *PACKAGES, venv=VENV)

    if OUTPUT and not ARGS.get('--no-install', False):
        FUNC = lambda x: x[0]
        OUTPUT.sort(key=FUNC, reverse=True)
        for _, pkg in OUTPUT:
            path = os.path.join(DIR_, pkg)
            # TODO : force yes for all (if option given)
            makepkg(path, install=True)
            DEBUG.info(path)

