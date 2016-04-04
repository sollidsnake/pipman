#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""function to generate PKGBUILD"""

import logging
import re
import os

from misc import VENV_DIR, VENV_PIP, ENCODING, DEVNULL
from misc import PYTHON_VERSION, blacklist

import pip_wrapper as pip

from venv_wrapper import *
from pkgbuild_parser import *

def generate_pkgbuild(package_info):
    """Generate PKGBUILD for package"""

    log = logging.getLogger("user")
    log.info("Generating pkgbuild for %s", package_info['pack'])

    # regex to match version and release
    ver_rel = re.search(r"(\d+(?:\.\d+)+)(?:-(\d+))?",
                        package_info['Version'])

    version = ver_rel.group(1)
    release = ver_rel.group(2)

    if not release:
        release = '1'

    # TODO : faire conflit avc pkgname
    # store the pkgbuild output variable in 'lines' var
    return open("PKGBUILD.tpl").read().format(
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
    #

def generate_dir(packages, prefix='.'):
    """ Generate directories"""
    # check if directories don't exist

    log = logging.getLogger("user")
    for pack in packages.values():
        dir_ = os.path.join(prefix, pack['pkgname'])
        if os.path.exists(dir_):
            log.error("Directory '%s' already exists", dir)
            quit() # TODO : meilleur check

        # store directory in package dict
        packages[pack['pack']]['dir'] = dir

def generate_pkgbuild_file(packages):
    """generate the package build and store in package/PKGBUILD"""

    for pack in packages.values():
        pkgbuild = generate_pkgbuild(pack)
        os.makedirs(pack['dir'])

        with open(os.path.join(pack['dir'], 'PKGBUILD'), 'w') as file_:
            file_.write(pkgbuild)

def generate_all(packages, prefix='.'):
    """Generate package/PKGBUILD for every package in self.packages"""
    generate_dir(packages, prefix)
    generate_pkgbuild_file(packages)


def install_packages(prefix, *packages):
    """ Install the packages """
    create_virtualenv()
    pkg = {}
    for k, package in parse_packages(*packages):
        pkg[k] = package
        # If there is dependencies, install them
        logging.getLogger("user").info("Installing %s", package['Name'])
        if package['Requires']:
            logging.getLogger("user").info("Installing dependencie %s", package['Requires'])
            install_packages(prefix, *[e for e in package['Requires'].split(",")])
        install_in_venv(package['Name'])
    generate_all(pkg, prefix) # TODO : voir d'où vient l'erreur

if __name__ == "__main__":
    create_virtualenv()
    for _, v in parse_packages("kademlia"):
        print("{}".format(generate_pkgbuild(v)))

