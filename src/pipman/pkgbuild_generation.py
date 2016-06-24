#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""function to generate PKGBUILD"""

import logging
import re
import os
import filecmp

from typing import Dict, List

from misc import VENV_DIR, VENV_PIP, ENCODING, DEVNULL
from misc import PYTHON_VERSION, blacklist

import pip

from venv import *
from pkgbuild_parser import *

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
            depends=" ".join(['"python-' + e + '"' for e in package_info['Requires'].split(', ') if e]),
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

def log_pkg_info(package: Dict[str, str]):
    logging.getLogger('user').info("dependencies: %s", package['Requires'])

# TODO : return tuple (dep level, pkgname) for installation (with pacman)
def install_packages(prefix: str, options: List, *packages, **kwargs):
    """ Install the packages """
    pkg_list = []
    dep_level = kwargs.get('deplevel', 0)
    for _, package in parse_packages(*packages):
        logging.getLogger('user').info("Installing %s", package['Name'])
        log_pkg_info(package) # TODO
        if package['Requires']:
            logging.getLogger('user').info("Installing dependencie %s", package['Requires'])
            pkg_list += install_packages(prefix,
                                         *[e for e in package['Requires'].split(", ")],
                                         deplevel=dep_level+1)
        install_in_venv(package['Name'])
        generate_pkg(package)

        # Append the dependancie depth (0 for the package installed by the
        # user, 1 for its dependencie ...)
        pkg_list.append((dep_level, package['pkgname']))
    return pkg_list

if __name__ == "__main__":
    install_packages('.', [], "kademlia")

