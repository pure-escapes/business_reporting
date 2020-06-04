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
import datetime

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

    def test_get_incomplete_tickets_on_main_board_for_a_specific_version(self):
        columns_of_main_board = [] #except backlog,done,closed
        project_name = 'OWA'
        version = "1.1.0"

        report_object = self.__j1.get_stories_and_bugs_tickets_that_are_in_progress_for_a_specific_version(project_name=project_name, version=version)
        formatted_output = json.dumps(report_object, indent=2)
        # print(formatted_output)

        self.__j1.print_short_message_for_update(report_object)


    def test_get_issues_by_issue_type_from_the_main_board_for_a_specific_version(self):
        project_name = 'OWA'
        version = "1.1.0"

        report_object = self.__j1.get_quality_from_the_main_board_for_a_specific_version(
            project_name=project_name, version=version)
        formatted_output = json.dumps(report_object, indent=2)
        print(formatted_output)

        self.__j1.print_short_message_for_quality_assessment(report_object)


    def test_get_issues_by_issue_type_from_the_backlog_for_a_specific_version(self):
        project_name = 'OWA'
        version = "1.2.0"

        report_object = self.__j1.get_quality_from_backlog_for_a_specific_version(
            project_name=project_name, version=version)
        formatted_output = json.dumps(report_object, indent=2)
        # print(formatted_output)

        self.__j1.print_short_message_for_quality_assessment(report_object)

    def test_assess_the_quality_of_multiple_versions_in_backlog(self):
        project_name = 'OWA'
        assessment_by_versions = {
                            "1.1.0":{},
                            "1.2.0":{},
                            "1.3.0":{},
                            "2.0.0":{}
                            }

        self.__j1.get_quality_of_multiple_versions(project_name, assessment_by_versions)



        formatted_output = json.dumps(assessment_by_versions, indent=2)
        print(formatted_output)



    def test_hours_booked_against_tickets_in_the_main_board_for_a_specific_week(self):
        project_name = 'OWA'
        target_versions = ["1.0.0","1.1.0", "1.2.0"]
        start_date = datetime.datetime(2020, 5, 25)
        end_date = datetime.datetime(2020, 5, 31)

        for version in target_versions:
            report_object = self.__j1.get_breakdown_of_tickets_with_hours_booked(start_date, end_date, project_name, version)

            # formatted_output = json.dumps(report_object, indent=2)
            # print(formatted_output)

            self.__j1.show_message_for_logged_work(report_object, True)
        #todo: this approach does not check if on a day a user booked 40d!!!! (but also possibly this might not be stored on jira's data model)

    def test_create_time_tracking(self):
        project_name = 'OWA'
        target_versions = ["1.0.0", "1.1.0", "1.2.0"]
        start_date = datetime.datetime(2020, 5, 1)
        end_date = datetime.datetime(2020, 5, 31)

        for version in target_versions:
            report_object = self.__j1.get_breakdown_of_tickets_with_hours_booked(start_date, end_date, project_name,
                                                                                 version)
            self.__j1.create_data_as_csv_for_logged_work_for(report_object, True)



    def test_get_which_tickets_had_pairing_and_collaboration_in_the_main_board_for_a_specific_week(self):
        #identify the ticket numbers, where the main assignee and another member had booked time
        pass

    def test_find_out_tickets_that_potentially_should_turn_to_epic_and_be_rescoped(self):
        pass

    def test_time_tracking_per_user_per_stack(self):

        #shared ticket = 1204 & shared epic 1625
        output = self.__j1.get_time_tracking_of_a_ticket_per_user('OWA-1625')

        print(json.dumps(output, sort_keys=True, indent=4, separators=(",", ": ")))

    def test_creating_agile_velocity_snapshot_for_business_reporting(self):
        project_name = 'OWA'
        target_versions = ["1.0.0", "1.1.0", "1.2.0"]
        start_date = datetime.datetime(2020, 5, 1)
        end_date = datetime.datetime(2020, 5, 31)


        report_object = self.__j1.get_a_list_of_DONE_tickets_within_a_period(start_date, end_date, project_name, target_versions)
        self.__j1.create_data_as_csv_for_DONE_tickets(report_object, True)


    def test_finding_the_date_a_ticket_started_being_developed(self):

        test_ticket = 'OWA-1564'
        expected_time = '2020/05/22'
        temp = self.__j1.calculate_the_cycle_time_of_an_issue_from_its_activity(test_ticket)
        found_time = temp.strftime('%Y/%m/%d')

        self.assertEqual(expected_time,found_time)


#todo filters: https://supermetrics.com/blog/google-data-studio-advanced-tips

# todo find any tickets without epics (in backlog & kanban board)
# todo do quality analysis of the kanban board
# todo calculate how to re-assign the work, so as to finish earlier, based on the availability of developers
# todo estimate lead time (for a ticket, for  particular version)
# todo estimate WIP (for a ticket to flow through the board)
# todo check tickets in the backlog (if the important information is missing; epic, version, story points, original estimation, etc)
# todo how many tickets finished in a week