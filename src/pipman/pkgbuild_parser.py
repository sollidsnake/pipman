#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Function for parsing result of pip show"""

import logging
import re

from typing import Dict

from misc import ENCODING, blacklist
import pip_wrapper as pip
import venv_wrapper as venv

def compile_package_info(package: str) -> Dict[str, str]:
    """Store 'pip show package' in dict"""

    log = logging.getLogger("user")
    log.info("Checking package info for %s", package)

    info = pip.show(package)

    # we need to encode terminal output
    info = info.decode(ENCODING)

    # regex to match the values before and after :
    info = re.findall(r"^([\w-]+): (.*)$", info, re.MULTILINE)

    info_dict = {}

    for k, val in info:
        info_dict[k] = val

    info_dict['pack'] = package
    info_dict['pkgname'] = "python-%s" % package.lower()

    return info_dict

def parse_packages(*packages) -> Dict[str, Dict[str, str]]:
    """ Parses packages """
    logging.getLogger("user").info("pkg : %s", packages)
    for pack in packages:
        logging.getLogger("user").info("Parsing %s", pack)
        venv.install_in_venv(pack)
        if pack not in blacklist:
            yield pack, compile_package_info(pack)


if __name__ == "__main__":
    for _, v in parse_packages("kad.py"):
        print(v)
