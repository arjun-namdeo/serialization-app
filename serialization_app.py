#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
#######################################################################################################################
                                            Serializer Application

Description :
    A command line tool which shows how you would take some sets of personal data  (seq, shot, frame, status)
    and serialise/de-serialize them into 2 formats ( PICKLE Format and JSON Format)

    and display it in at least 2 different ways  (HTML Output and TEXT Output)

    You could manually pass the arguments or use the Template CSV file to use as in input.

    This package has been written in such a way that it would be easy for a developer:
    * To add support for additional storage formats   (Easily extend in  /scripts/encoder.py )
    * To query a list of currently supported formats
    * To supply an alternative reader/writer for one of the supported formats  ( Find in /scripts/display_output.py )

    Please check unit_test.py for API Examples as well.


Usage :
    Run from command line

        python serialization_app.py    # This will use default_template_database and generate output
        or
        python serialization_app.py -seq 010 -shot 200 -frame 78   # This will use user input and show in browser

#######################################################################################################################
"""

__author__ = 'Arjun Prasad Namdeo'


import config
from scripts import common, encoder, display_output, parser

map(reload, [config, common, encoder, display_output, parser])

from scripts.common import io


def get_supported_serializer_formats():
    """
    Get all the current supported serializer class formats

    :return  `dict`   With name of the serializer class and the class object itself
    """
    return encoder.get_supported_serializer_formats()

def get_supported_output_formats():
    """
    Get all the current supported serializer class formats

    :return  `dict`   With name of the serializer class and the class object itself
    """
    raise display_output.get_supported_output_formats()


class SerializerApp(object):
    """
    Main serialization application class

    You can use following command to execute the serializer

        app = SerializerApp()
        app.run()


    """
    def __init__(self):
        super(SerializerApp, self).__init__()
        # append package directory to sys.path so that all modules can be loaded
        config.update_sys_path()

    def run(self):
        """
        Main execution method to running serializer. This method will execute following processes.

            *   It will fetch the user inputs and validate them. If validation fails, Process will stop.

            *   It will generate user_data_context. user_data_context is basically a DataStructure which
                can be read by different serializer classes.

            *   It will serialize the user_data in JSON and PICKLE file format. Those files will get saved in the
                user directory. It will also show the file path in terminal. You can find the path file from terminal.

            *   It will generate display output in HTML and TEXT File format. File paths will be showed in terminal.

        """
        # parse user inputs and validate them
        user_inputs = parser.UserInputs()

        # validate the user input
        if not user_inputs.validate():
            io.error("Validation Failed. Please check your inputs.!")
            return False
        io.info("Validation Done. All okay. Proceeding ahead. ")

        # Build the data_context as per user input. This data can be read by different serializer classes.
        # You can pass this data_context to any serializer class.
        user_data = user_inputs.build_context()

        # Do the JSON serializations with user data context
        json_serializer = encoder.JsonSerializer(data=user_data)
        json_serialized_file = json_serializer.encode()

        ''' Un-comment below line, If you want to decode the serialized json file. '''
        # json_serializer.decode(filePath=json_serialized_file)

        # Do the PICKLE serializations with user data context
        pickle_serializer = encoder.PickleSerializer(data=user_data)
        pickle_serialized_file = pickle_serializer.encode()

        ''' Un-comment below line, If you want to decode the serialized pickle file. '''
        # pickle_serializer.decode(filePath=pickle_serialized_file)

        ''' Generate Display Output for user '''
        # generate the HTML Display output for user with current context data
        html_exporter = display_output.HtmlExporter(data=user_data)
        html_file = html_exporter.export()

        # open the html file in default browser
        #common.view_file(file_path=html_file)

        # generate the TEXT Display output for user with current context data
        text_exporter = display_output.TextExporter(data=user_data)
        text_file = text_exporter.export()

        # open the text file in default browser
        #common.view_file(file_path=text_file)

        io.info("Process complete...!!!")
        return True


def launch_program():
    app = SerializerApp()
    app.run()


if __name__ == '__main__':
    launch_program()


