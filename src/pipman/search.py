#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pip search function wrapper
"""

import re

import logging
from functools import reduce
from typing import List

from pip2 import search

from color import colorize, ForeGround, BackGround

# TODO : check if package is installed out of pip (??)

def format_packages(package: str, desc: str, installed: bool) -> str:
    """Format package information (from pip search) like pacman output"""

    return """{python}/{name}{installed}
    {desc}""".format(python=colorize('python', ForeGround.red),
                     name=package,
                     desc=desc,
                     installed=" " + colorize("(installed)",
                                              ForeGround.black,
                                              BackGround.yellow) if installed else "")

def parse_search(pkg: str) -> str:
    """perform pip search for the package and format the output"""
    tmp = search(pkg)
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

def search_and_fmt(packages: List[str]) -> str:
    """search and format packages"""
    return reduce(lambda e, acc: e + "\n" + acc, [parse_search(e) for e in packages])

def search_and_print(packages: List[str]):
    """print output of search"""
    # TODO : print in log ???
    print(search_and_fmt(packages))

if __name__ == "__main__":
    print(search(['kad']))
