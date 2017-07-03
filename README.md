# Description
Pipman generates PKGBUILD from pip packages. You can use the generated
PKGBUILD as a base to submit a new python package to AUR or just
install it on you machine.

# Installation
You can install:
- using the aur package: https://aur4.archlinux.org/packages/pipman-git/
- cloning this repo and running the `./pipman`

Install the `colorama` module if you want to colorize the output

# Usage
The following generates PKGBUILDs for `MechanicalSoup` and `pyrasite` packages from pip:
```
pipman MechanicalSoup pyrasite
```
Then you should see the directories `python-MechanicalSoup` and `python-pyrasite` in the current directory, each containing its PKGBUILD.

You can also specify where you want the PKGBUILDs to be generated:
```
pipman MechanicalSoup pyrasite --target-dir=/tmp/
```

You can search for pip packages with the argument `-Ss`:
```
pipman -Ss sympy
```

You can install the generated PKGBUILD automatically with the argument `-S`:
```
pipman -S sympy
```

Check `pipman --help` for more features.

# Todo
There are a few missing features I plan to implement:
- option to update the packages installed with pipman automatically

# Credits
- Thanks to [n3f4s](https://github.com/n3f4s) for the auto-install feature.
