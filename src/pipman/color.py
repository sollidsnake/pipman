#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Color module cf http://stackoverflow.com/a/29723536"""

class PrintInColor:
    """PrintInColor"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_PURPLE = '\033[94m'
    PURPLE = '\033[95m'
    END = '\033[0m'

    @classmethod
    def red(cls, s, **kwargs):
        return "{}".format(cls.RED + s.format(**kwargs) + cls.END)

    @classmethod
    def green(cls, s, **kwargs):
        return "{}".format(cls.GREEN + s + cls.END, **kwargs)

    @classmethod
    def yellow(cls, s, **kwargs):
        return "{}".format(cls.YELLOW + s.format(**kwargs) + cls.END)

    @classmethod
    def lightPurple(cls, s, **kwargs):
        return "{}".format(cls.LIGHT_PURPLE + s.format(**kwargs) + cls.END)

    @classmethod
    def purple(cls, s, **kwargs):
        return "{}".format(cls.PURPLE + s.format(**kwargs) + cls.END)
