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

from reportGenerators.UpdaterOfGoogleSpreadSheetsFromJira import UpdaterOfGoogleSpreadSheetsFromJira

class Test_JIRAFetcher(unittest.TestCase):

    def test_get_bugs_for_a_specific_version(self):
        status = False

        u532 = UpdaterOfGoogleSpreadSheetsFromJira()

        status = u532.update()


        self.assertTrue(status)