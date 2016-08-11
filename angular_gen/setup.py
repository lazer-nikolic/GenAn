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
import os

__author__ = "Lazar Nikolić <lazarpwna AT gmail DOT com>, Bojana Zoranović, Dragoljub Ilić"
__version__ = "0.1.0.dev1"

from setuptools import setup, find_packages

NAME = 'GenAn Angular'
VERSION = __version__
DESC = 'AngularJS generator based on GenAn DSL'
AUTHOR = __author__
AUTHOR_EMAIL = '<lazarpwna AT gmail DOT com>'
LICENSE = 'MIT'
URL = 'https://github.com/theshammy/GenAn'

# Load all template files in form:
# [folder_path: [file1_path, file2_path... ]]
data_files = [
    ("/{0}".format(entry[0]), [os.path.join(entry[0], file) for file in entry[2]]) for entry in os.walk('templates')
]

data_files.append(('/', ['app.zip']))

setup(
    name=NAME,
    version=VERSION,
    description=DESC,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    license=LICENSE,
    url=URL,
    py_modules=['angular_generator', 'jinja_filters'],
    keywords='genan angular generator dsl',
    data_files=data_files,
    install_requires=[
        'textx',
        'arpeggio',
        'jinja2',
        'Click'
    ],
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
    entry_points={
        'genan.frontend_generator': [
            'generator=angular_generator:AngularGenerator',
        ]
    },
)
