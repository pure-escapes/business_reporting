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

from reportGenerators.UpdaterOfGoogleSpreadSheetsFromJira import UpdaterOfGoogleSpreadSheetsFromJira

class Test_JIRAFetcher(unittest.TestCase):

    def get_filepath_from_resouces_starting_from_tests_directory(self, target_filename):
        here = __file__
        path_to_tests, this_file = os.path.split(here)
        path_to_root, dummy = os.path.split(path_to_tests)
        path_to_target_file = os.path.join(path_to_root, 'resources', target_filename)

        return path_to_target_file


    def test_calculations_from_a_single_file(self):
        status = False
        configuration = None

        path_to_target_file = self.get_filepath_from_resouces_starting_from_tests_directory('basefile_of_UpdaterConfiguration.json')
        with open(path_to_target_file, "r") as read_file:
            configuration = json.load(read_file)

            configuration["input"]["at_the_start_of_the_period"]["backlog_size"] = 68
            configuration["input"]["at_the_start_of_the_period"]["tickets_committed"] = 10
            configuration["input"]["at_the_start_of_the_period"]["capacity_ratio_for_bugs"] = 6

            configuration["input"]["at_the_end_of_the_period"]["tickets_completed"] = 5
            configuration["input"]["at_the_end_of_the_period"]["tickets_added_to_backlog_during_the_period"] = 1
            configuration["input"]["at_the_end_of_the_period"]["bugs_added_to_backlog_during_the_period"] = 2
            configuration["input"]["at_the_end_of_the_period"]["tickets_removed_from_backlog_during_the_period"] = 3


            configuration["google_settings"]["path_to_configuration_file_to_google_spreadsheet"] = self.get_filepath_from_resouces_starting_from_tests_directory("simple_reports_configuration.json")


        u532 = UpdaterOfGoogleSpreadSheetsFromJira(configuration)

        status = u532.update()

        output = u532.calculate()

        self.assertEqual(output["team_velocity"], 5)
        self.assertAlmostEqual(output["estimated_days_to_complete"], 12.6)
        self.assertAlmostEqual(output["weighted_iterations_to_complete"], 13.4 )
        self.assertAlmostEqual(output["relative_difference_between_estimation_and_weighted_iterations"], 6.35)




        # self.assertTrue(status)
        self.assertTrue(configuration!=None)