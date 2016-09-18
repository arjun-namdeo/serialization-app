#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Module for displaying the output for Serialized data
"""

__author__ = 'Arjun Prasad Namdeo'

import os
import config

from collections import OrderedDict
from scripts.common import io, validate_file_path

output_registry = dict()

def get_supported_output_formats():
    """
    get all the supported serialization formats at the current api
    """
    registered_items = output_registry.keys()
    message = 'Totally {0} output formats are supported. Find more info at "/scripts/exporters.py"'
    io.info(message.format(len(registered_items)))
    io.info("Registered Serializers : {0}".format(registered_items))
    return output_registry


def register_class(target_class):
    """
    Method for register classes available for serialization process.
    """
    output_registry[target_class.__name__] = target_class
    return target_class


class RegisterMetaClass(type):
    """
    Base metaclass to store class registry information
    """
    def __new__(cls, class_name, bases, attributes):
        new_class = super(RegisterMetaClass, cls).__new__(cls, class_name, bases, attributes)
        register_class(new_class)
        return new_class


class Exporter(object):
    """
    Abstracted class for Export process. This should be used as base class for all the exporters

    HtmlExporter() and TextExporter() are good inherited examples.
    """

    EXPORT_TYPE = None
    EXPORT_FILE_NAME = None

    def __init__(self, data):
        self.data = data

    def get_context(self):
        return self.data

    def convert_data2string(self):
        raise NotImplemented

    def export(self):
        """
        Method for the main export process. Needs to be implemented in inherited classes
        """
        raise NotImplemented

    @property
    def export_path(self):
        """
        temporary display output file path.
        """

        export_path = os.path.join(config.OUTPUT_DIRECTORY, self.EXPORT_FILE_NAME)
        return export_path


class HtmlExporter(Exporter):
    """
    HTML Exporter will generate a output display page in HTML Format where all the user data can be shown

    This class has export() method which will generate the physical file at user directory
    """
    # Register this class
    __metaclass__ = RegisterMetaClass

    EXPORT_TYPE = "HTML"
    EXPORT_FILE_NAME = "{0}.html".format(config.OUTPUT_FILE_NAME)

    def convert_data2string(self, data=None):
        """
        Method to convert the user_data into HTML Exporter formatted string
        """
        information = data or self.get_context()

        _head_string = ""
        _data_string = ""
        _header_updated = False
        for each_info in information:
            _data_string += "\t\t<tr>\n\t\t\t"
            for heading, data in OrderedDict(each_info).iteritems():
                _data_string += "<td align='center'> %s </td>\n\t\t\t" % data
                if _header_updated:
                    continue
                _head_string += "<th> %s </th>\n\t\t" % heading
            _header_updated = True
            _data_string += "\n\t\t</tr>\n"

        html_string = """
<!DOCTYPE html>
<html>
<head>
<title>Serialized data in HTML display</title>
</head>
<body>
<table border=1, style="width:60%", align="center">
<caption style="color:red"><B>Output in HTML Format - Total Entries : {NUM}</B></caption>
    <tr>
        {HEAD}
    </tr>
     <indent>
{DATA}
     </indent>
</table>
</body>
</html>
"""
        return html_string.format(HEAD=_head_string, DATA=_data_string, NUM=len(information))

    def export(self, filePath=None, data=None):
        """
        main export method
        """
        export_file_path = filePath or self.export_path

        if not validate_file_path(file_path=export_file_path, file_extension=".html"):
            return None

        html_string = data or self.convert_data2string()

        with open(export_file_path, "w") as htmlWriter:
            htmlWriter.write(html_string)

        io.info("Display output has been created in %s Format. Output Saved here :  %s " % (self.EXPORT_TYPE,
                                                                                            export_file_path))
        return export_file_path



class TextExporter(Exporter):
    """
    TEXT Exporter will generate a output display in TEXT format where all the user data can be shown

    This class has export() method which will generate the physical file at user directory
    """

    # Register this class
    __metaclass__ = RegisterMetaClass

    EXPORT_TYPE = "TEXT"
    EXPORT_FILE_NAME = "{0}.txt".format(config.OUTPUT_FILE_NAME)

    def convert_data2string(self, data=None):
        """
        Method to convert the user_data into Text Exporter formatted string
        """
        information = data or self.get_context()

        text_string = ""
        text_string += "**********  Output in TEXT Format  ************* \n\n"
        text_string += "Total inputs received :  %s \n" % len(information)
        text_string += "------------------------------------------------\n"

        for each_info in information:
            for heading, data in OrderedDict(each_info).iteritems():
                text_string += "\t{0}\t\t=\t{1} \n".format(heading, data)
            text_string += "\n"
            text_string += "------------------------------------------------\n"
        return text_string

    def export(self, filePath=None, data=None):
        """
        main export method
        """

        export_file_path = filePath or self.export_path

        if not validate_file_path(file_path=export_file_path, file_extension=".txt"):
            return None

        text_string = data or self.convert_data2string()

        with open(export_file_path, "w") as textWriter:
            textWriter.write(text_string)

        io.info("Display output has been created in %s Format. Output Saved here :  %s " % (self.EXPORT_TYPE,
                                                                                            export_file_path))
        return export_file_path


