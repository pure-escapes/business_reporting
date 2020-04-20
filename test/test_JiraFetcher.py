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

from reportGenerators.JiraFetcher import JIRA_Fetcher

class Test_JIRAFetcher(unittest.TestCase):

    def test_get_bugs_for_a_specific_version(self):
        number_of_bugs = 0

        j1 = JIRA_Fetcher()
        number_of_bugs = j1.get_number_of_bugs_in_backlog_for('OWA', '1.1.0')


        self.assertGreater(number_of_bugs, 0)