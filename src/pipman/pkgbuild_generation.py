#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""function to generate PKGBUILD"""

import logging

from typing import Dict, List

from pkgbuild_parser import parse_packages
import printer

def log_pkg_info(package: Dict[str, str]):
    """log some imfos"""
    logging.getLogger('user').info("dependencies: %s", package['Requires'])

def dep_of(pkg):
    """list dependencies of pkg"""
    return [e for e in pkg['Requires'].split(", ")]

def install_packages(prefix: str, *packages, **kwargs):
    """ Install the packages """
    pkg_list = []
    dep_level = kwargs.get('deplevel', 0)
    venv_ = kwargs['venv']

    for _, package in parse_packages(venv_, *packages):

        logging.getLogger('user').info("Installing %s", package['Name'])
        log_pkg_info(package) # TODO

        if package['Requires']:

            logging.getLogger('user').info("Installing dependencie %s", package['Requires'])

            pkg_list += install_packages(prefix, *dep_of(package),
                                         deplevel=dep_level+1, venv=venv_)
        venv_.install_in_venv(package['Name'])
        printer.generate_pkg(package)

        # Append the dependancie depth (0 for the package installed by the
        # user, 1 for its dependencie ...)
        pkg_list.append((dep_level, package['pkgname']))
    return pkg_list

if __name__ == "__main__":
    install_packages('.', [], "kademlia")

