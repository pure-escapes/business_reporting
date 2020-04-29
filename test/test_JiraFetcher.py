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
import json

from reportGenerators.JiraFetcher import JIRA_Fetcher

class Test_JIRAFetcher(unittest.TestCase):

    def setUp(self) -> None:

        self.__j1 = JIRA_Fetcher()

    def test_get_bugs_for_a_specific_version(self):
        number_of_bugs = 0


        number_of_bugs = self.__j1.get_number_of_bugs_in_backlog_for('OWA', '1.1.0')


        self.assertGreater(number_of_bugs, 0)

    def test_get_backlog_size_for_a_specific_version_of_a_project_and(self):
        backlog_size = 0

        backlog_size = self.__j1.get_size_of_backlog_for('OWA', '1.1.0')

        self.assertGreater(backlog_size, 0)

    def test_how_many_tickets_closed_within_a_time_range(self):
        backlog_size = 0

        backlog_size = self.__j1.get_tickets_completed_within_period('OWA', '2020/04/01', '2020/04/20', '1.0.0')

        self.assertEqual(backlog_size, 10)

    def test_get_incomplete_tickets_on_main_board(self):
        columns_of_main_board = [] #except backlog,done,closed
        project_name = 'OWA'
        version = "1.1.0"

        t = self.__j1.get_stories_and_bugs_tickets_that_are_in_progress_for_a_specific_version(project_name=project_name, version=version)
        formatted_output = json.dumps(t, indent=2)
        print(formatted_output)
        #all lowercase, replace

