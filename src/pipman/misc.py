import os
import locale
import re
import subprocess

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
PYTHON_VERSION = re.search(" (\d+\.\d+)",
                           subprocess
                           .check_output(["python", '--version'])
                           .decode(ENCODING)).group(1)
