import os
import locale
import sys

# packages that souldn't be generated
blacklist = []

# get system encoding
ENCODING = locale.getdefaultlocale()[1]

# get system null device
DEVNULL = open(os.devnull, 'w')

# tmp directories
TMP_DIR = os.path.join(os.path.sep, 'tmp', 'pipman')
VENV_DIR = os.path.join(TMP_DIR, 'pipman-venv')
VENV_PIP = os.path.join(VENV_DIR, 'bin/pip')

# get python version from system, only the first two numbers
PYTHON_VERSION = "%d.%d" % (sys.version_info.major, sys.version_info.minor)
