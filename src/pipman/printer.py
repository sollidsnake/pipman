#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Print PKGBUILD"""

import os
import logging
import re
from typing import Dict

from misc import PYTHON_VERSION

def generate_pkgbuild(package_info: Dict[str, str]) -> str:
    """Generate PKGBUILD for package"""

    log = logging.getLogger('user')
    log.info("Generating pkgbuild for %s", package_info['pack'])

    # regex to match version and release
    ver_rel = re.search(r"(\d+(?:\.\d+)+)(?:-(\d+))?",
                        package_info['Version'])

    version = ver_rel.group(1)
    release = ver_rel.group(2)

    if not release:
        release = '1'

    # store the pkgbuild output variable in 'lines' var
    with open('PKGBUILD.tpl') as file_:
        return file_.read().format(
            aut=package_info['Author'],
            authmail=package_info['Author-email'],
            pkgname=package_info['pkgname'],
            pkgver=version,
            pkgrel=release,
            pkgdesc=package_info['Summary'],
            url=package_info['Home-page'],
            license=package_info['License'],
            depends=" ".join(['"python-' + e + '"'
                              for e in package_info['Requires'].split(', ') if e]),
            pack=package_info['pack'],
            pyversion=PYTHON_VERSION)

def create_dir(pkgname: str, prefix='.') -> str:
    """create destination dir and return the path

    if destination dir already exists, do nothing (except logging)
    and return the path"""

    # TODO : check if directory exists (without the pkgname)
    dest = os.path.join(prefix, pkgname)
    if not os.path.exists(dest):
        logging.getLogger('user').info("Creating directory %s", dest)
        os.makedirs(dest)
    else:
        logging.getLogger('user').info("Directory %s already exists", dest)
    return dest

def write_pkgbuild(package: Dict[str, str]):
    """write the PKGBUILD on a file"""
    dest = os.path.join(package['dir'], 'PKGBUILD')

    with open(dest, 'w') as file_:
        logging.getLogger('user').info("Writing PKGBUILD at %s", dest)
        file_.write(generate_pkgbuild(package))


def generate_pkg(package: Dict[str, str], prefix='.'):
    """Generate the destination dir and write pkgbuild"""
    package['dir'] = create_dir(package['pkgname'], prefix)
    write_pkgbuild(package)
