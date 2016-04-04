#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import venv
import os

from misc import VENV_DIR, VENV_PIP

import pip_wrapper as pip

def create_virtualenv():
    """Create virtualenv to install packages"""

    log = logging.getLogger("user")
    log.info("Preparing virtualenv")

    if not os.path.exists(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)
        log.info('checking for pip upgrade') # upgrade pip
        pip.install('pip', '-U', in_venv=True)

def install_in_venv(package):
    """Install package in virtualenv"""

    log = logging.getLogger("user")
    log.info("Installing '%s' in virutalenv", package)

    # install package in virtualenv pip
    pip.install(package, "--disable-pip-version-check", "--no-dependencies", in_venv=True)

