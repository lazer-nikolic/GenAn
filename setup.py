#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# Name: genan.py
# Purpose: PEG parser interpreter
# Author: ILazar Nikolić <lazarpwna AT gmail DOT com>, Bojana Zoranović, Dragoljub Ilić
# Copyright: (c) 20016 Lazar Nikolić <lazarpwna AT gmail DOT com>, Bojana Zoranović, Dragoljub Ilić
# License: MIT License
#
# GenAn is a DSL for definition of client-side application based on AngularJS.
###############################################################################

__author__ = "Lazar Nikolić <lazarpwna AT gmail DOT com>, Bojana Zoranović, Dragoljub Ilić"
__version__ = "0.1.0.dev1"

from setuptools import setup

NAME = 'GenAn'
VERSION = __version__
DESC = 'DSL for definition of client-side application based on AngularJS'
AUTHOR = __author__
AUTHOR_EMAIL = '<lazarpwna AT gmail DOT com>'
LICENSE = 'MIT'
URL = 'https://github.com/theshammy/GenAn'
# DOWNLOAD_URL = 'https://github.com/igordejanovic/Arpeggio/archive/v{}.tar.gz'\
#     .format(VERSION)

setup(
    name = NAME,
    version = VERSION,
    description = DESC,
    author = AUTHOR,
    author_email = AUTHOR_EMAIL,
    maintainer = AUTHOR,
    maintainer_email = AUTHOR_EMAIL,
    license = LICENSE,
    url = URL,
    # download_url = DOWNLOAD_URL,
    packages = ["src"],
    scripts = ['src/main/genan.py'],
    keywords = "dsl angular mean",
    install_requires=['textx', 'arpeggio'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
        ],


)