#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""
from jira import JIRA
import re
import requests

import os

def try_with_standard_HTML():
    url = "https://pureescapes.atlassian.net"
    body = {
        "username": os.getenv("PE_JIRA_USERNAME"),
        "password": os.getenv("PE_JIRA_BI_LISTENER")
    }
    headers = {"content_type": "application/json"}
    r = requests.post(url, data=body, headers=headers)
    print(r.text)

def attempt_3():
    jira = JIRA(os.getenv("PE_JIRA_URI"), basic_auth=(os.getenv("PE_JIRA_USERNAME"), os.getenv("PE_JIRA_BI_LISTENER")))

    # print all of the project keys as an example
    for project in jira.projects():
        print(project.key)

def hello():
    # By default, the client will connect to a JIRA instance started from the Atlassian Plugin SDK
    # (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
    # Override this with the options parameter.
    options = {"server": "https://pureescapes.atlassian.net"}
    # print(os.getenv("PE_JIRA_USERNAME"), os.getenv("PE_JIRA_PASSWORD"))
    # jira = JIRA(options)
    j1 = JIRA(options, basic_auth=(os.getenv("PE_JIRA_USERNAME"), os.getenv("PE_JIRA_BI_LISTENER")))
    ticket = 'OWA-1400'
    issue = j1.issue(ticket)

    summary = issue.fields.summary

    print('ticket: ', ticket, summary)

if __name__ == "__main__":
    # hello()
    # try_with_standard_HTML()
    attempt_3()