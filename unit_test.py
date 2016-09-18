#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit test module for Serialization Application
"""

__author__ = 'Arjun Prasad Namdeo'

import unittest

from scripts import parser, encoder, display_output, common


class TestSerializer(unittest.TestCase):
    """
    Unit Test class for serializer
    """

    def setup_user_data(self):
        # provide some shot information
        shotInfo_A = {'sequence': 'A20', 'shot': 'sh500', 'frames': 167, 'artist': 'Josh'}
        return shotInfo_A

    def test_serializer(self):
        user_data = self.setup_user_data()
        user_data = parser.UserInputs.build_data_container(data=user_data)

        # Test JSON Serializer
        json_serializer = encoder.JsonSerializer(data=user_data)
        json_serialized_file = json_serializer.encode()

        json_deserialized_data = json_serializer.decode(filePath=json_serialized_file)

        self.assertEqual(user_data, json_deserialized_data)

        # Test Pickle Serializer
        pickle_serializer = encoder.PickleSerializer(data=user_data)
        pickle_serialized_file = pickle_serializer.encode()

        pickle_deserialized_data = pickle_serializer.decode(filePath=pickle_serialized_file)

        self.assertEqual(user_data, pickle_deserialized_data)

        ''' Generate Display Output for user '''
        # generate the HTML Display output for user with current context data
        html_exporter = display_output.HtmlExporter(data=user_data)
        html_file = html_exporter.export()

        # open the html file in default browser
        common.view_file(file_path=html_file)

        # generate the TEXT Display output for user with current context data
        text_exporter = display_output.TextExporter(data=user_data)
        text_file = text_exporter.export()

        # open the text file in default browser
        common.view_file(file_path=text_file)


if __name__ == '__main__':
    unittest.main()