#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import os
import json
import requests

import datetime
import os

import json, requests, pprint
from requests.auth import HTTPBasicAuth

def get_coverage_for_component(component_name: str):
    '''

    :param component_name: as it appears on sonarcloud
    :return: float (which is a percentage already)
    '''

    url = 'https://sonarcloud.io/api/measures/component_tree'

    query = {'component': component_name,
             'metricKeys': "coverage",
             'ps': 100,
             'p': 1}
    r = requests.get(url, params=query, auth=(os.environ['PE_BUSINESS_REPORT_TOKEN'], ''))
    metrics_dict = r.json()

    formatted_output = json.dumps(metrics_dict, indent=2)
    # print(formatted_output)

    coverage_value = 0.0
    if metrics_dict["baseComponent"]["measures"][0]["metric"] == "coverage":
        coverage_value = float(metrics_dict["baseComponent"]["measures"][0]["value"])

    print("coverage for "+component_name+":", str(coverage_value), "%")
    return coverage_value

