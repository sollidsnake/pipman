# Description
Pipman generates PKGBUILD from pip packages.

# Installation
You can install:
- using the aur package: https://aur4.archlinux.org/packages/pipman-git/
- cloning this repo and running the `./pipman`

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

As of version 0.9.1 you can search for pip packages with the argument `-s`:
```
pipman -s sympy
```

# Todo
There are a few missing features I plan to implement:
- option to install generated PKGBUILDs automatically
- try to integrate with pip dependencies
- better info output
- currently works with python3 only
