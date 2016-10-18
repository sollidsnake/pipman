import subprocess
from misc import ENCODING


def search(packages: list):
    out = subprocess.check_output(['pip', 'search', packages[0]])\
                    .decode(ENCODING)
    print(out)
