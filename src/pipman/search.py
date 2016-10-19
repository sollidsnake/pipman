import subprocess
from misc import ENCODING


def search(packages: list):
    packages_join = " ".join(packages)
    out = subprocess.check_output(['pip', 'search', packages_join])\
                    .decode(ENCODING)

    print(out)
