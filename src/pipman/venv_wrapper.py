#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper function for venv function"""

import logging
import venv
import os

from misc import VENV_DIR, VENV_PIP

import pip_wrapper as pip

_VENV_CREATED = False

def create_virtualenv():
    """Create virtualenv to install packages"""

    log = logging.getLogger("user")
    log.info("Preparing virtualenv")

    if not os.path.exists(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)
        log.info('checking for pip upgrade') # upgrade pip
        pip.install('pip', '-U', in_venv=True)
    global _VENV_CREATED
    _VENV_CREATED = True

def install_in_venv(package: str):
    """Install package in virtualenv"""

    if not _VENV_CREATED or not os.path.exists(VENV_DIR):
        create_virtualenv()
    log = logging.getLogger("user")
    log.info("Installing '%s' in virutalenv at %s", package, VENV_DIR)

    # install package in virtualenv pip
    pip.install(package, "--disable-pip-version-check", "--no-dependencies", in_venv=True)
