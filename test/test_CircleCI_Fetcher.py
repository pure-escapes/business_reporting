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


class Test_CircleCI_Fetcher(unittest.TestCase):

    def test_get_successful_jobs_of_a_specific_project_that_started_within_a_specific_period(self):
        '''
        BLOCKED: left ticket with CircleCI https://support.circleci.com/hc/en-us/requests/72023
        :return:
        '''

        selected_year = 2020
        selected_month = 3
        start_date = 2
        end_date = 1

        token_value = os.environ.get('PE_CIRCLECI_API_TOKEN')
        headers = {
            'Circle-Token': token_value,
        }

        params = (
            ('branch', 'sandbox'),
        )

        response = requests.get(
            'https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs/deploy_sandbox',
            headers=headers, params=params)

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs/deploy_sandbox?branch=sandbox', headers=headers)


        print(response.text)

        data_to_parse = response.json()['items']

        counter_of_jobs = 0
        counter_of_successful_jobs = 0
        for job in data_to_parse:
            date = parse(job["started_at"])

            if (job["status"] == "success") and (date.month == selected_month) and (date.year == selected_year):
                print(job['id'], date.date(), date.month, date.year)
                counter_of_successful_jobs += 1
            counter_of_jobs += 1

        efficiency = round(100.0 * counter_of_successful_jobs / counter_of_jobs, 2)
        print("in", selected_month,'total deployments(as jobs):', counter_of_jobs, "(", efficiency ,"% successful)")

    #todo use PycURL instead of `requests`
