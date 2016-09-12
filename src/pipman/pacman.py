#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python wrapper for pacman and makepkg"""

import subprocess
import os
import logging

def makepkg(pkg_path: str, *args, **kwargs):
    """wrapper around makepkg"""

    install = ''
    if kwargs.get('install', False):
        install = 'i'

    current_dir = os.getcwd()

    logging.getLogger('user').info('moving to %s', pkg_path)

    os.chdir(pkg_path)

    subprocess.check_call(['makepkg', "-s{}".format(install)] + list(args))

    logging.getLogger('debug').info('makepkg -s%s %s', install, " ".join(['-'+elt for elt in args]))
    logging.getLogger('user').info('leaving %s', pkg_path)

    os.chdir(current_dir)
