#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper function for venv function"""

import logging
import venv
import os
import shutil

# from misc import VENV_DIR, VENV_PIP

import pip2

_VENV_CREATED = False


class Venv(object):

    """Wrapper around venv"""

    def __init__(self, path: str, **kwargs):
        self._path = path
        self._user_log = logging.getLogger("user")
        self._created = False
        self._clean = kwargs.get('always_clean', False)
        self._user_log.info("Preparing virtualenv")
        if not os.path.exists(self._path):
            venv.create(self._path, with_pip=True)
            self._user_log.info('checking for pip upgrade')  # upgrade pip
            pip2.install('pip', '-U', venv_path=self._path)
        elif not kwargs.get('force', True):
            raise Exception("Directory {} already exists".format(self._path))
        self._created = True

    def __enter__(self):
        return self

    def __del__(self):
        if self._clean:
            self.clean()

    def __exit__(self, exc_type, exc_value, traceback):
        if self._clean:
            self.clean()

    @property
    def path(self):
        """property for path"""
        return self._path

    def install_in_venv(self, package: str):
        """Install package in virtualenv"""
        self._user_log.info("Installing '%s' in virutalenv at %s",
                            package,
                            self._path)
        try:
            pip2.install(package, "--disable-pip-version-check",
                         "--no-dependencies", venv_path=self.path)
        except pip2.PackageNotFound as exc:
            self.clean()
            raise exc

    def clean(self):
        """clean tmp files (usefull if venv not fully installed)"""
        self._user_log.info("Cleaning %s", self._path)
        shutil.rmtree(self._path)
