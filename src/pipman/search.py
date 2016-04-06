#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pip search function wrapper
"""

import re

from functools import reduce
from typing import List

import pkgbuild_parser as parser
import pip_wrapper as pip

from color import PrintInColor

# TODO : check if package is installed out of pip (??)

def format_packages(package: str, desc: str, installed: bool) -> str:
    """Format package information (from pip search) like pacman output"""

    return """{python}/{name}{installed}
    {desc}""".format(python=PrintInColor.red('python'),
                     name=package,
                     desc=desc,
                     installed=PrintInColor.purple(" (installed)") if installed else "")

def parse_search(pkg: str) -> str:
    """perform pip search for the package and format the output"""
    tmp = pip.search(pkg)
    if not tmp:
        return ""
    result = ""
    for idx, line in enumerate(tmp):
        grp = re.match(r"(.*)\s\((?:\d*\.?)+\)\s*\-\s(.*)", line)
        if grp:
            installed = idx+1 < len(tmp) and "INSTALLED" in tmp[idx+1]
            if idx+1 < len(line):
                pass
            result += format_packages(grp.group(1), grp.group(2), installed) + "\n"
    return result

def search(packages: List[str]) -> str:
    """search and format packages"""
    return reduce(lambda e, acc: e + "\n" + acc, [parse_search(e) for e in packages])

def search_and_print(packages: List[str], options: List):
    """print output of search"""
    # TODO : print in log ???
    print(search(packages))

if __name__ == "__main__":
    print(search(['kad']))
