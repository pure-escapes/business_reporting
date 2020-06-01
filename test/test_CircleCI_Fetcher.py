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
import requests

import dateutil
from dateutil.parser import parse

from reportGenerators.CircleCI_Fetcher import CircleCI_Fetcher
import calendar


class Test_CircleCI_Fetcher(unittest.TestCase):

    def setUp(self) -> None:

        self.__c1 = CircleCI_Fetcher()


    def test_get_successful_jobs_of_a_specific_project_that_started_within_a_specific_period(self):
        '''
        BLOCKED: left ticket with CircleCI https://support.circleci.com/hc/en-us/requests/72023
        :return:
        '''

        start_date_as_str = "1/4/2020"
        end_date_as_str = "29/4/2020"

        config = {}
        config["start_date_as_str"] = start_date_as_str
        config["end_date_as_str"] = end_date_as_str
        config["circleCI_project"] = "webapp-backend"
        config["name_of_job_that_deploys_to_production"] = "deploy_sandbox"
        config["name_of_github_branch_related_to_production"] = "sandbox"

        self.__c1.get_deployments_of_a_branch_within_a_specific_range_of_dates(config)

    def test_check_the_most_important_branches_between_to_dates(self):
        start_date_as_str = "18/5/2020"
        end_date_as_str = "22/5/2020"

        config = self.__c1.get_basic_configuration_file()
        config["start_date_as_str"] = start_date_as_str
        config["end_date_as_str"] = end_date_as_str
        report_object = self.__c1.check_several_branches(config)

        self.__c1.show(report_object)

    def test_check_the_most_important_branches_for_a_particular_month(self):
        selected_month = 4
        selected_year = 2020

        start_date_as_str = "1/"+str(selected_month)+"/"+str(selected_year)
        last_day = str(calendar.monthrange(selected_year, selected_month)[1])
        end_date_as_str = last_day+"/"+str(selected_month)+"/"+str(selected_year)

        config = self.__c1.get_basic_configuration_file()
        config["start_date_as_str"] = start_date_as_str
        config["end_date_as_str"] = end_date_as_str


        report_object = self.__c1.check_several_branches(config)

        self.__c1.show(report_object)


    def test_progress_over_particular_months(self):
        months = [1,2,3,4]
        selected_year = 2020

        for selected_month in months:
            start_date_as_str = "1/" + str(selected_month) + "/" + str(selected_year)
            last_day = str(calendar.monthrange(selected_year, selected_month)[1])
            end_date_as_str = last_day + "/" + str(selected_month) + "/" + str(selected_year)

            config = self.__c1.get_basic_configuration_file()
            config["start_date_as_str"] = start_date_as_str
            config["end_date_as_str"] = end_date_as_str

            report_object = self.__c1.check_several_branches(config)

            self.__c1.show(report_object)

