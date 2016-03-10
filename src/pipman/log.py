"""Simple wrapper around logging"""

import logging
import sys


class Log():
    """Simple wrapper around logging"""

    def __init__(self):
        self.log = logging.getLogger()
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("pipman: %(message)s")
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)
        self.log.setLevel(logging.INFO)

    def info(self, msg):
        """log message with info level"""
        self.log.info(msg)

    def error(self, msg):
        """log message with error level"""
        self.log.error(msg)
