import logging
import sys


class Log():

    def __init__(self):
        self.log = logging.getLogger()
        sh = logging.StreamHandler(sys.stderr)
        sh.setLevel(logging.INFO)
        format = logging.Formatter("pipman: %(message)s")
        sh.setFormatter(format)
        self.log.addHandler(sh)
        self.log.setLevel(logging.INFO)

    def info(self, msg):
        self.log.info(msg)

    def error(self, msg):
        self.log.error(msg)

    def set_level(self, level):
        self.log.setLevel(level)
