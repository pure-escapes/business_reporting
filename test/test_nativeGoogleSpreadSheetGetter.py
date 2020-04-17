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

from reportGenerators.GoogleSpreadSheetGetterWithNativeGoogleAPI import NativeGoogleSpreadSheetGetter

class TestCaseGoogleSpreadSheetGetter(unittest.TestCase):

    def test_reading_data(self):
        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "spread_sheet_specifics_for_test_report45.json")

        g7 = NativeGoogleSpreadSheetGetter(path_to_filename)
        temp_data = g7.get_values_from_spreadsheet()
        self.assertTrue(len(temp_data) > 0)

        g7.show_data()

class TestCaseGoogleSpreadSheetGetter_with_bad_input(unittest.TestCase):
    def test_not_having_configuration_file_for_reports(self):

        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "this_file_does_not_exist.json")

        with self.assertRaises(FileNotFoundError) as cm:
            g1 = NativeGoogleSpreadSheetGetter(path_to_filename)

        self.assertEqual(cm.exception.errno, 2)

    def test_that_the_reports_configuration_does_not_point_to_a_valid_google_credentials_path(self):

        current_directory, this_file = os.path.split(__file__)
        one_directory_above, name_of_current_directory = os.path.split(current_directory)
        path_to_filename = os.path.join(one_directory_above,"resources", "bad_input_with_non_existing_google_credentials_file.json")

        with self.assertRaises(OSError) as cm:
            g1 = NativeGoogleSpreadSheetGetter(path_to_filename)

        self.assertEqual(cm.exception.errno, 1)





