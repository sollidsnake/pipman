#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""function to generate PKGBUILD"""

import logging

from typing import Dict, List

from pkgbuild_parser import parse_packages
import printer

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

