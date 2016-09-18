#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module for parsing data from user
"""

__author__ = 'Arjun Prasad Namdeo'

import argparse
from collections import OrderedDict

import config
from scripts.common import io, readCsv, validate_file_path


def get_args():
    """
    this will parse the information from terminal and return a argparse.namespace object to the caller
    """
    # create argument parser
    parser = argparse.ArgumentParser(description='Retrieves user inputs for Shot definition')

    parser.add_argument('--external_file',
                        type=str, help='Provide an external CSV file path for reading the data.',
                        required=False)

    parser.add_argument('-use_template', '--use_default_template', dest='useTemplateData', action='store_true',
                        help="Set this to True If you want default template data.")
    parser.set_defaults(useTemplateData=False)

    parser.add_argument('-seq', '--sequence', type=str, help='Enter Sequence Name', required=False)
    parser.add_argument('-shot', '--shot', type=str, help='Enter Shot Name', required=False)
    parser.add_argument('-frame', '--frames', type=int, help='Enter frame count', required=False, default=1)
    parser.add_argument('-artist', '--artist', type=str, help='Enter Artist Name', required=False, default="Unassigned")

    return parser.parse_args()


class UserInputs(object):
    """
    Fetch user inputs from terminal
    """

    def __init__(self):
        super(UserInputs, self).__init__()
        self.user_args = None
        self._information = None

    def getInput(self):
        """
        get user inputs from the terminal. Main called to the argparse
        """
        self.user_args = get_args()
        return self.user_args

    def validate(self, inputs=None):
        """
        This will check all the user inputs and validate them and put them in information variable
        """
        io.info("Validating Inputs...")
        inputs = inputs or self.getInput()

        information = OrderedDict()

        if not all([inputs.sequence, inputs.shot, inputs.frames, inputs.artist]):
            io.warn("Values for all fields are not provided. Using external data file If any.")
            inputs.useTemplateData = True

        if self.validate_string(string=inputs.sequence):
            information["sequence"] = inputs.sequence

        if self.validate_string(string=inputs.shot):
            information["shot"] = inputs.shot

        if self.validate_int(value=inputs.frames):
            information["frames"] = inputs.frames

        if self.validate_string(string=inputs.artist):
            information["artist"] = inputs.artist

        external_file = None
        if inputs.useTemplateData:
            external_file = config.TEMPLATE_DATABASE

        elif inputs.external_file:
            external_file = inputs.externalFilePath

        if external_file:
            if validate_file_path(file_path=external_file, file_extension=".csv",
                                  check_existence=True):
                information["filePath"] = external_file
                io.info("Using user data from file at :  %s " % external_file)

        self._information = OrderedDict(information)
        return information

    def build_context(self, information=None):
        """
        collect all the information from the user and external files and keep them in one place
        """
        information = information or self._information or self.validate()
        if not information:
            return None
        build_data = self.build_data_container(data=information)
        return build_data

    def validate_int(self, value):
        return str(value).isdigit()

    def validate_string(self, string):
        return bool(string)

    @classmethod
    def build_data_container(cls, data):
        """
        Generate a data structure context which can be read by any serializer class
        """
        data_container = list()
        file_to_read = data.get('filePath', None)

        if file_to_read:
            # Using external file to fetch input
            read_information = list(readCsv(filePath=file_to_read))
            if not read_information:
                return data_container

            headers = read_information.pop(0)
            for data in read_information:
                local_dict = OrderedDict(zip(headers, data))
                data_container.append(local_dict)
        else:
            data_container.append(OrderedDict(data))

        return data_container

