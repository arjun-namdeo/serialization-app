#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Module Docs
"""

__author__ = 'Arjun Prasad Namdeo'

# import python in-built module(s)
import os
import json
import pickle

# import self-package module(s)
import config
from scripts.common import io, validate_file_path

# Creating registry to store all the serialization format classes
registry = dict()

def get_supported_serializer_formats():
    """
    get all the supported serialization formats at the current api
    """
    registered_items = registry.keys()
    message = 'Totally {0} formats are supported in current Serializer. Find more info at "/scripts/encoder.py"'
    io.info(message.format(len(registered_items)))
    io.info("Registered Serializers : {0}".format(registered_items))
    return registry


def register_class(target_class):
    """
    Method for register classes available for serialization process.
    """
    registry[target_class.__name__] = target_class
    return target_class


class RegisterMetaClass(type):
    """
    Base meta-class to store class registry information

    You can add following lines to any class and those classes will get registered in SerializerRegistry.
    """
    def __new__(cls, class_name, bases, attributes):
        new_class = super(RegisterMetaClass, cls).__new__(cls, class_name, bases, attributes)
        register_class(new_class)
        return new_class


class Serializer(object):
    """
    Abstracted base class for serializer

    This has methods for encoding/decoding the different type of serializer formats
    You can use this class as base class and define your own Serializer

        Extension example : JsonSerializer() and PickleSerializer()
    """

    TEMP_FILE_NAME = None
    TEMP_FILE_EXT = None

    def __init__(self, data):
        super(Serializer, self).__init__()
        self.dataToWrite = data

    @property
    def temporary_filePath(self):
        """
        temporary file path for saving the serialized data
        """
        filePath = os.path.join(config.OUTPUT_DIRECTORY, self.TEMP_FILE_NAME)
        return filePath

    def encode(self):
        """
        Method for encode/serialize the user data. Needs to be implemented in inherited classes
        """
        raise NotImplementedError

    def decode(self):
        """
        Method for decode/de-serialize the user data. Needs to be implemented in inherited classes
        """
        raise NotImplementedError


class JsonSerializer(Serializer):
    """
    JSON Serializer class. This has methods for encode/decode the user inputs

    This is a inherited class of Serializer
    """

    # Register this class
    __metaclass__ = RegisterMetaClass

    INDENT = 4
    TEMP_FILE_EXT = ".json"
    TEMP_FILE_NAME = "{0}{1}".format(config.SERIALIZE_FILE_NAME, TEMP_FILE_EXT)

    def __init__(self, data=None):
        super(JsonSerializer, self).__init__(data)

    def encode(self, filePath=None):
        """
        Method for encode/serialize the user data in Json format. This will save
        a json file format in user directory.

        The location will get printed in the user's console/terminal

        :return  `str`   File path of serialized file.
        """

        file_to_serialization = filePath or self.temporary_filePath
        file_to_serialization = file_to_serialization.replace("\\", "/")

        if not validate_file_path(file_path=file_to_serialization, file_extension=self.TEMP_FILE_EXT):
            return None

        with open(file_to_serialization, "w") as writeFile:
            json.dump(self.dataToWrite, writeFile, indent=self.INDENT)

        io.info("")
        io.info("Serialization Done in JSON Format. Serialized data saved here :  %s \n" % file_to_serialization)
        return file_to_serialization

    @classmethod
    def decode(cls, filePath=None):
        """
        Method for decode/de-serialize the user data. You can pass and external json File here.

        This method will read the file with json_reader
        """

        file_to_serialization = filePath or cls.temporary_filePath
        file_to_serialization = file_to_serialization.replace("\\", "/")

        if not validate_file_path(file_path=file_to_serialization, file_extension=cls.TEMP_FILE_EXT,
                                  check_existence=True):
            return None

        with open(file_to_serialization, "r") as readFile:
            data = json.load(readFile)
        return data


class PickleSerializer(Serializer):
    """
    Pickle Serializer class. This has methods for encode/decode the user inputs

    This is a inherited class of Serializer
    """
    # Register this class
    __metaclass__ = RegisterMetaClass

    TEMP_FILE_EXT = ".pickle"
    TEMP_FILE_NAME = "{0}{1}".format(config.SERIALIZE_FILE_NAME, TEMP_FILE_EXT)

    def __init__(self, data):
        super(PickleSerializer, self).__init__(data)

    def encode(self, filePath=None):
        """
        Method for encode/serialize the user data in Json format. This will save
        a pickle file format in user directory.

        The location will get printed in the user's console/terminal

        :return  `str`   File path of serialized file.

        """

        file_to_serialization = filePath or self.temporary_filePath
        file_to_serialization = file_to_serialization.replace("\\", "/")

        if not validate_file_path(file_path=file_to_serialization, file_extension=self.TEMP_FILE_EXT):
            return None

        with open(file_to_serialization, "wb") as writeFile:
            pickle.dump(self.dataToWrite, writeFile)

        io.info("")
        io.info("Serialization Done in PICKLE Format. Serialized data saved here :  %s \n" % file_to_serialization)
        return file_to_serialization

    @classmethod
    def decode(cls, filePath=None):
        """
        Method for decode/de-serialize the user data
        """

        file_to_serialization = filePath or cls.temporary_filePath
        file_to_serialization = file_to_serialization.replace("\\", "/")

        if not validate_file_path(file_path=file_to_serialization, file_extension=cls.TEMP_FILE_EXT,
                                  check_existence=True):
            return None

        with open(file_to_serialization, "rb") as readFile:
            data = pickle.load(readFile)
        return data


