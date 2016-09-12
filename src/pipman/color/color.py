#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities for terminal coloration"""

import sys

from enum import Enum

class Style(Enum):
    """Enum for terminal style of printing"""
    reset = 0
    bright = 1
    dim = 2
    underline = 3
    # blink = 4 => what is the use of this character ?
    blink = 5
    reverse = 6
    hidden = 7

class ForeGround(Enum):
    """Enum for the foreground color of the font in the terminal"""
    black = 30
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37

class BackGround(Enum):
    """Enum for the background color of the font in the terminal"""
    black = 40
    red = 41
    green = 42
    yellow = 43
    blue = 44
    magenta = 45
    cyan = 46
    white = 47

def colorize(string, foreground, background=BackGround.black, style=Style.reset) -> str:
    """return the string with the color terminal code"""
    if sys.stdout.isatty:
        col = '\x1b[{}m'.format(';'.join([str(style.value),
                                          str(foreground.value), str(background.value)]))
        reset = '\x1b[0m'
        return "{col}{str_}{clear}".format(col=col, str_=string, clear=reset)
    else:
        return string

if __name__ == "__main__":
    print(colorize("Youpi Banane ! ", ForeGround.blue, BackGround.magenta, Style.underline))
