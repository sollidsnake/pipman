#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""function to generate PKGBUILD"""

import subprocess
import re
import os
import venv

from misc import VENV_DIR, VENV_PIP, ENCODING, DEVNULL
from misc import PYTHON_VERSION, blacklist
from log import Log

def create_virtualenv():
    """Create virtualenv to install packages"""
    # Pip2Pkgbuild.log.info("Preparing virtualenv")

    if os.path.exists(VENV_DIR):
        return

    venv.create(VENV_DIR, with_pip=True)

    # upgrade pip
    # Pip2Pkgbuild.log.info('checking for pip upgrade')
    subprocess.check_call([VENV_PIP, 'install', '-U', 'pip'])

def install_in_venv(package):
    """Install package in virtualenv"""
    # Pip2Pkgbuild.log.info("Installing '%s' in virutalenv" % package)

    # install package in virtualenv pip
    subprocess.check_call([VENV_PIP,
        'install',
        '--disable-pip-version-check',
        '--no-dependencies',
        package])
    #

def compile_package_info(package):
    """Store 'pip show package' in dict"""
    # Pip2Pkgbuild.log.info("Checking package info")

    info = subprocess.check_output([VENV_PIP, 'show', package],
            stderr=DEVNULL)

    # we need to encode terminal output
    info = info.decode(ENCODING)

    # regex to match the values before and after :
    info = re.findall(r"^([\w-]+): (.*)$", info, re.MULTILINE)

    info_dict = {}

    for i in info:
        info_dict[i[0]] = i[1]

    info_dict['pack'] = package
    info_dict['pkgname'] = "python-%s" % package.lower()

    return info_dict

def parse_packages(*packages):
    """ Parses packages """
    for pack in packages:
        if pack not in blacklist:
            yield pack, compile_package_info(pack)


def generate_pkgbuild(package_info):
    """Generate PKGBUILD for package"""
    Pip2Pkgbuild.log.info("Generating pkgbuild for %s"
            % package_info['pack'])

    # regex to match version and release
    ver_rel = re.search(r"(\d+(?:\.\d+)+)(?:-(\d+))?",
            package_info['Version'])

    version = ver_rel.group(1)
    release = ver_rel.group(2)

    if not release:
        release = '1'

    # store the pkgbuild output variable in 'lines' var
    return open("PKGBUILD.tpl").read().format(
            aut=package_info['Author'],
            authmail=package_info['Author-email'],
            pkgname=package_info['pkgname'],
            pkgver=version,
            pkgrel=release,
            pkgdesc=package_info['Summary'],
            url=package_info['Home-page'],
            license=package_info['License'],
            depends=" ".join(['"python-' + e + '"' for e in package_info['Requires'].split(', ') if e]),
            pack=package_info['pack'],
            pyversion=PYTHON_VERSION)
    #

def generate_dir(packages, prefix='.'):
    """ Generate directories"""
    # check if directories don't exist
    for pack in packages.values():
        dir_ = os.path.join(prefix, pack['pkgname'])
        if os.path.exists(dir_):
            # Pip2Pkgbuild.log.error("Directory '%s' already exists" % dir)
            quit()

        # store directory in package dict
        packages[pack['pack']]['dir'] = dir

def generate_pkgbuild_file(packages):
    """Write the PKGBUILD file"""
    # generate the package build and store in package/PKGBUILD
    for pack in packages.values():
        pkgbuild = generate_pkgbuild(pack)
        os.makedirs(pack['dir'])

        with open(os.path.join(pack['dir'], 'PKGBUILD'), 'w') as file_:
            file_.write(pkgbuild)

def generate_all(packages, prefix='.'):
    """Generate package/PKGBUILD for every package in self.packages"""
    generate_dir(packages, prefix)
    generate_pkgbuild_file(packages)


def install_packages(prefix, *packages):
    """ Install the packages """
    create_virtualenv()
    for package in parse_packages(*packages):
        # If there is dependencies, install them
        if package['Require']:
            install_packages(*package['Require'])
        install_in_venv(package['Name'])
        generate_all(package, prefix)


