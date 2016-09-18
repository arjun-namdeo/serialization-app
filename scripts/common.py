#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Module for all the common methods
"""

__author__ = 'Arjun Prasad Namdeo'

import os
import csv
import webbrowser

def readCsv(filePath):
    """
    CSV File reader
    """
    if not validate_file_path(file_path=filePath):
        return

    with open(filePath, "r") as csv_read:
        reader = csv.reader(csv_read, delimiter=',', quotechar='|')
        for row in reader:
            yield row


def validate_file_path(file_path, file_extension=None, check_existence=False):
    """
    common method for validating a file_path

    @:param `file_path`         `str`   : Provide file path which you want to validate
    @:param `file_extension`    `str`   : Set this If you want to validate a specific file type. like .csv or .json
    @:param `check_existence`   `bool`  : Set this True/False if you want to check physical existence of file

    """
    if not file_path:
        io.warn('No File Path received. Please provide correct filePath')
        return False

    if file_extension:
        if not str(file_path).endswith(str(file_extension)):
            io.warn('Invalid File Type. Please provide a filePath with "{0}" file format.'.format(file_extension))
            return False

    if check_existence:
        if not os.path.isfile(file_path):
            io.warn("File NOT Found. File %s does not found in location." % file_path)
            return False

    return True


def view_file(file_path=None):
    """
    Open up the file path in default browser.
    """
    if not validate_file_path(file_path=file_path, check_existence=True):
        return

    try:
        webbrowser.open("file://" + file_path)
    except Exception, e:
        io.warn("Cannot start file because {0}.  File Path : {1}".format(e, file_path))


class io(object):
    """
    Simple Class for echoing the output with different color.

    This class have following methods which will echo messages in terminal in their respective colors

        io.warn(message)  :   "YELLOW" Color        (For any warning)
        io.info(message)  :   "GREEN" Color         (For any success)
        io.error(message) :   "RED" Color           (For any critical error)
        io.echo(message)  :   "DEFAULT" Color       (Normal message)

    """

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

    @classmethod
    def warn(cls, message):
        string = "{COLOR} WARN :  {MSG}{RESET}".format(COLOR=cls.YELLOW, MSG=str(message), RESET=cls.RESET)
        print(string)

    @classmethod
    def info(cls, message):
        string = "{COLOR} INFO :  {MSG}{RESET}".format(COLOR=cls.GREEN, MSG=str(message), RESET=cls.RESET)
        print(string)

    @classmethod
    def error(cls, message):
        string = "{COLOR} ERROR :  {MSG}{RESET}".format(COLOR=cls.RED, MSG=str(message), RESET=cls.RESET)
        print(string)

    @classmethod
    def echo(cls, message, prefix=">>>"):
        string = "{PRE} {MSG}{RESET}".format(PRE=prefix, MSG=str(message), RESET=cls.RESET)
        print(string)
