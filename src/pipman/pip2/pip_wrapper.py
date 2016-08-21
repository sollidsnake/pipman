#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper around pip commands"""

import subprocess
import logging
import os
import locale

from typing import List

VERSION = 3

__PIP = {3 : "pip", 2 : "pip2"}

DEVNULL = open(os.devnull, 'w')

ENCODING = locale.getdefaultlocale()[1]

class PackageNotFound(Exception):
    """pkg not found exception"""
    def __init__(self, pkg):
        Exception.__init__()
        self._pkg = pkg

    def pretty_print(self):
        """ pretty print"""
        return "Target {} was not found".format(self._pkg)

def show(package: str, **kwargs) -> str:
    """wrapper around pip show"""
    pip = 'pip'
    venv_path = kwargs.get('venv_path', None)
    if venv_path:
        pip = os.path.join(venv_path, 'bin/pip')
    try:
        return subprocess.check_output([pip, 'show', package], stderr=DEVNULL)
    except subprocess.CalledProcessError:
        raise PackageNotFound(package)


def search(package: str) -> List[str]:
    """wrapper around pip search"""
    try:
        logging.getLogger('debug').info("%s %s %s", 'pip', 'search', package)
        tmp = subprocess.check_output(['pip', 'search', package])
    except subprocess.CalledProcessError:
        return None
    return tmp.decode(ENCODING).split('\n')

def install(package: str, *args, **kwargs):
    """wrapper around pip install"""
    pip = 'pip'
    venv_path = kwargs.get('venv_path', None)
    if venv_path:
        pip = os.path.join(venv_path, 'bin/pip')
    logging.getLogger('debug').debug("%s", format([pip, 'install'] + list(args) + [package]))
    try:
        subprocess.check_call([pip] + ['install'] + list(args) + [package])
    except subprocess.CalledProcessError:
        raise PackageNotFound(package)
