#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import unittest

from reportGenerators.simpleGoogeSpreadSheetInterface import simpleGoogleSpreadSheetGetter

class TestCaseGoogleSpreadSheetGetter(unittest.TestCase):

    def test_reading_data(self):
        finame_of_configuration = "simple_reports_configuration.json"
        g17 = simpleGoogleSpreadSheetGetter(finame_of_configuration)
        temp_data = g17.get_values_from_spreadsheet()
        self.assertTrue(len(temp_data) > 0)

        g17.show_data()

class TestCaseGoogleSpreadSheetGetter_with_bad_input(unittest.TestCase):
    def test_not_having_all_files(self):


        with self.assertRaises(OSError) as cm:
            g1 = simpleGoogleSpreadSheetGetter("this_file_does_not_exist.json")

        self.assertEqual(cm.exception.errno, 1)


