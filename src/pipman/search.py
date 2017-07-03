import subprocess
from misc import ENCODING
import re
from pip2pkgbuild import Pip2Pkgbuild

PYTHON_PACKAGE_RE = '[._\w-]+'
PYTHON_VERSION_RE = '([^ ]*)'


def search(packages: list, color=True, pacman_like_output=True):
    """searches packages in pipman repo and display"""
    packages_join = " ".join(packages)
    out = subprocess.check_output(['pip', 'search', packages_join])\
                    .decode(ENCODING)

    # remove whitespace
    out = out.strip()

    # format pipman output to pacman output
    if pacman_like_output:
        out = re.sub(r'^(%s) \(%s\)\s+- ' % (PYTHON_PACKAGE_RE, PYTHON_VERSION_RE),
                     r'\1 \2\n    ',
                     out,
                     flags=re.MULTILINE)

        if color:
            out = _colorize(out)

    print(out)


def _colorize(output):
    """colorizes using pacman's colors"""
    try:
        from colorama import init, Fore
    except ModuleNotFoundError:
        Pip2Pkgbuild.log.warn("Install colorama module to colorize the output\n")
        return output
        
    init()
    output = re.sub(r'^(%s) %s' % (PYTHON_PACKAGE_RE, PYTHON_VERSION_RE),
                    r'%s\1%s %s\2%s' % (Fore.MAGENTA,
                                          Fore.RESET,
                                          Fore.CYAN,
                                          Fore.RESET),
                    output,
                    flags=re.MULTILINE)

    return output
