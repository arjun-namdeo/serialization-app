#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Common configuration module where all the constants
and global variables exists.
"""

__author__ = 'Arjun Prasad Namdeo'


import os
import sys

PACKAGE_DIRECTORY = os.path.dirname(__file__)

TEMPLATE_DATABASE = os.path.join(PACKAGE_DIRECTORY, "database/default_template_database.csv")

OUTPUT_DIRECTORY = os.path.join(PACKAGE_DIRECTORY, "output_files")

SERIALIZE_FILE_NAME = "serialized_data"
OUTPUT_FILE_NAME = "display_output"

for directory in [OUTPUT_DIRECTORY, OUTPUT_DIRECTORY]:
    if not os.path.isdir(directory):
        os.makedirs(directory)


def update_sys_path():
    sys.path.append(PACKAGE_DIRECTORY)

