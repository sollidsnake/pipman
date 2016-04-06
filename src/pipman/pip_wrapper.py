#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper around pip commands"""

import subprocess
import logging

from typing import List

from misc import DEVNULL, VENV_PIP, ENCODING

def show(package: str, **kwargs) -> str:
    """wrapper around pip show"""
    if kwargs.get('in_venv', False):
        return subprocess.check_output(['pip', 'show', package], stderr=DEVNULL)
    else:
        return subprocess.check_output([VENV_PIP, 'show', package], stderr=DEVNULL)

def search(package: str) -> List[str]:
    """wrapper around pip search"""
    pip = 'pip'
    tmp = ""
    try:
        tmp = subprocess.check_output([pip, 'search', package])
    except subprocess.CalledProcessError:
        return None
    return tmp.decode(ENCODING).split('\n')

def install(package: str, *args, **kwargs):
    """wrapper around pip install"""
    pip = 'pip'
    if kwargs.get('in_venv', False):
        pip = VENV_PIP
    logging.getLogger('debug').debug("%s", format([pip, 'install'] + list(args) + [package]))
    subprocess.check_call([pip] + ['install'] + list(args) + [package])
