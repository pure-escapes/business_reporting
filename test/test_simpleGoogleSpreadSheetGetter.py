#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import unittest
import os

from reportGenerators.simpleGoogeSpreadSheetInterface import simpleGoogleSpreadSheetGetter

class TestCaseGoogleSpreadSheetGetter(unittest.TestCase):

    def test_reading_data(self):
        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "simple_reports_configuration.json")


        g17 = simpleGoogleSpreadSheetGetter(path_to_filename)
        temp_data = g17.get_values_from_spreadsheet()
        self.assertTrue(len(temp_data) > 0)

        g17.show_data()

class TestCaseGoogleSpreadSheetGetter_with_bad_input(unittest.TestCase):
    def test_not_having_all_files(self):
        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "bad_simple_reports_configuration.json")

        with self.assertRaises(OSError) as cm:
            g1 = simpleGoogleSpreadSheetGetter(path_to_filename)

        self.assertEqual(cm.exception.errno, 1)

    def test_not_having_configuration_file_for_reports(self):

        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "this_file_does_not_exist.json")

        with self.assertRaises(FileNotFoundError) as cm:
            g1 = simpleGoogleSpreadSheetGetter(path_to_filename)

        self.assertEqual(cm.exception.errno, 2)


