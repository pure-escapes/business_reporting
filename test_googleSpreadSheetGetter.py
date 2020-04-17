#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import unittest
import http.client
import pprint
import json
import os
import pytest

from GoogleSpreadSheetGetter import GoogleSpreadSheetGetter

class TestCaseGoogleSpreadSheetGetter(unittest.TestCase):

    def test_reading_data(self):
        g7 = GoogleSpreadSheetGetter("spread_sheet_specifics_for_test_report45.json")
        temp_data = g7.get_values_from_spreadsheet()
        self.assertTrue(len(temp_data) > 0)

        g7.show_data()

class TestCaseGoogleSpreadSheetGetter_with_bad_input(unittest.TestCase):
    def test_not_having_all_files(self):

        with self.assertRaises(OSError) as cm:
            g1 = GoogleSpreadSheetGetter("this_file_does_not_exist.json")

        self.assertEqual(cm.exception.errno, 1)


