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

from GoogleSpreadSheetGetter import GoogleSpreadSheetGetter

class TestCaseGoogleSpreadSheetGetter(unittest.TestCase):

    def test_reading_data(self):
        g1 = GoogleSpreadSheetGetter("spread_sheet_specifics_for_test_report45.json")
        temp_data = g1.get_values_from_spreadsheet()
        self.assertTrue(len(temp_data) > 0)

        g1.show_data()
