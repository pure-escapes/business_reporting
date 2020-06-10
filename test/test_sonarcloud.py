#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, June 2020

"""
#some ideas could be used by https://github.com/kako-nawao/python-sonarqube-api

import unittest
import os
import json
import requests

import datetime
import os

import json, requests, pprint
from requests.auth import HTTPBasicAuth

class Test_Sonarcloud(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_1(self):
        #PE_SONAR_TOKEN_FOR_BUSINESS_REPORT_TOKEN

        url = 'https://sonarcloud.io/api/measures/component_tree'
        # query = {'component': 'keyJabref4.2', 'metricKeys': 'sqale_index', 'ps': 100, 'p': 1}
        query = {'user': os.environ['PE_BUSINESS_REPORT_TOKEN'],
                 'component': 'pure-escapes_pdf-service',
                 'metricKeys': 'sqale_index',
                 'ps': 100,
                 'p': 1}
        r = requests.get(url, params=query)
        metrics_dict = r.json()

        print(metrics_dict)



        url = url + '?component='+query['component']+"&metricKeys="+query['metricKeys']
        print('URL2:', url)
        myToken = os.environ['PE_BUSINESS_REPORT_TOKEN']

        session = requests.Session()
        session.auth = myToken, ''

        call = getattr(session, 'get')
        res = call(url)
        print(res.status_code)

        binary = res.content
        output = json.loads(binary)
        pprint.pprint(output)



    def test_basic_example(self):
        url = 'https://sonarcloud.io/api/measures/component_tree'

        query = {'component': 'pure-escapes_pdf-service',
                 'metricKeys': 'sqale_index',
                 'ps': 100,
                 'p': 1}
        r = requests.get(url, params=query, auth=(os.environ['PE_BUSINESS_REPORT_TOKEN'], ''))
        metrics_dict = r.json()

        formatted_output = json.dumps(metrics_dict, indent=2)
        print(formatted_output)

    def test_get_some_metrics(self):
        url = 'https://sonarcloud.io/api/metrics/search'

        query = {'component': 'pure-escapes_pdf-service',
                 'metricKeys': 'sqale_index',
                 'ps': 100,
                 'p': 1}
        r = requests.get(url, params=query, auth=(os.environ['PE_BUSINESS_REPORT_TOKEN'], ''))
        metrics_dict = r.json()

        formatted_output = json.dumps(metrics_dict, indent=2)
        print(formatted_output)


    def test_get_coverage_for_pdf_service(self):

        url = 'https://sonarcloud.io/api/measures/component_tree'

        query = {'component': 'pure-escapes_pdf-service',
                 'metricKeys': "coverage",
                 'ps': 100,
                 'p': 1}
        r = requests.get(url, params=query, auth=(os.environ['PE_BUSINESS_REPORT_TOKEN'], ''))
        metrics_dict = r.json()

        formatted_output = json.dumps(metrics_dict, indent=2)
        # print(formatted_output)

        coverage_value = 0.0
        if metrics_dict["baseComponent"]["measures"][0]["metric"] == "coverage":
            coverage_value = metrics_dict["baseComponent"]["measures"][0]["value"]

        print("coverage found:", coverage_value)