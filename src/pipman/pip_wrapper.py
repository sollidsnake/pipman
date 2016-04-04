#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""wrapper around pip commands"""

import subprocess

from misc import DEVNULL, VENV_PIP

def show(package, **kwargs):
    """wrapper around pip show"""
    if not kwargs.get('in_venv', False):
        return subprocess.check_output(['pip', 'show', package], stderr=DEVNULL)
    else:
        return subprocess.check_output([VENV_PIP, 'show', package], stderr=DEVNULL)

def search(package):
    """wrapper around pip search"""
    pip = 'pip'
    tmp = ""
    try:
        tmp = subprocess.check_output([pip, 'search', package])
    except subprocess.CalledProcessError:
        return None
    return tmp.decode('utf-8').split('\n')

def install(package, *args, **kwargs):
    """wrapper around pip install"""
    pip = 'pip'
    if not kwargs.get('in_venv', False):
        pip = VENV_PIP
    print("{}".format([pip] + list(args) + [package]))
    subprocess.check_call([pip] + ['install'] + list(args) + [package])
