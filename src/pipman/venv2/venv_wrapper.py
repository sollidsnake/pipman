#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper function for venv function"""

import logging
import venv
import os
import shutil

from misc import VENV_DIR, VENV_PIP

import pip as pip

_VENV_CREATED = False


class Venv(object):

    """Wrapper around venv"""

    def __init__(self, path: str, force=True):
        self._path = path
        self._user_log = logging.getLogger("user")
        self._created = False
        self._user_log.info("Preparing virtualenv")
        if not os.path.exists(self._path):
            venv.create(self._path, with_pip=True)
            self._user_log.info('checking for pip upgrade')  # upgrade pip
            pip.install('pip', '-U', in_venv=True)
        elif not force:
            raise Exception("Directory {} already exists".format(self._path))
        self._created = True

    def __enter__(self):
        return self

    def __del__(self):
        self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        self.clean()

    @property
    def path(self):
        """property for path"""
        return self._path

    def install_in_venv(self, package: str):
        """Install package in virtualenv"""
        self._user_log.info("Installing '%s' in virutalenv at %s", package, self._path)
        pip.install(package, "--disable-pip-version-check",
                    "--no-dependencies", venv_path=self.path)

    def clean(self):
        """clean tmp files (usefull if venv not fully installed)"""
        self._user_log.info("Cleaning", self._path)
        shutil.rmtree(self._path)


def create_virtualenv():
    """Create virtualenv to install packages"""

    log = logging.getLogger("user")
    log.info("Preparing virtualenv")

    if not os.path.exists(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)
        log.info('checking for pip upgrade')  # upgrade pip
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
    pip.install(package, "--disable-pip-version-check",
                "--no-dependencies", in_venv=True)
