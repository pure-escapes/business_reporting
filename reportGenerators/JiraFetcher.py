#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""
from jira import JIRA, Issue
import re
import requests
import json
import os
import datetime


class JIRA_Fetcher:
    __jira_handler = None
    __project_name = None
    __version = None

    def __init__(self, project_name:str = None, version:str = None):
        '''

        :param project_name: as it appears on jira e.g., "OWA"
        :param version: as it appears on jira e.g., "1.1.0"
        '''
        options = {"server": "https://pureescapes.atlassian.net"}
        # print(os.getenv("PE_JIRA_USERNAME"), os.getenv("PE_JIRA_PASSWORD"))
        # jira = JIRA(options)
        self.__jira_handler = JIRA(options=options, basic_auth=(os.getenv("PE_JIRA_USERNAME"), os.getenv("PE_JIRA_BI_LISTENER")))
        if project_name is not None:
            self.__project_name = project_name

        if version is not None:
            self.__version = version

    def get_now_as_a_string(self):
        now_time_object = datetime.datetime.now()
        return now_time_object.strftime("%Y%m%d_%H%M")


    def get_number_of_bugs_in_backlog_for(self, project_name, version):
        bugs_found = 0

        template_of_JQL_command = "issuetype in (Bug) AND project = {} AND fixVersion = {} AND status = Backlog"

        JQL_command = template_of_JQL_command.format(project_name, version)

        results = self.__jira_handler.search_issues(JQL_command, startAt=0, maxResults=200)
        bugs_found = len(results)
        return bugs_found

    def get_size_of_backlog_for (self, project_name, version):
        tickets_found = 0

        template_of_JQL_command = "issuetype in (Bug, Story) AND project = {} AND fixVersion = {} AND status = Backlog"
        JQL_command = template_of_JQL_command.format(project_name, version)

        results = self.__jira_handler.search_issues(JQL_command, startAt=0, maxResults=200)

        tickets_found = len(results)
        return tickets_found

    def get_tickets_completed_within_period(self, project_name, start_date, end_date, version):
        tickets_found = 0

        template_of_JQL_command = 'project = "{}" AND issuetype in (Bug,Story) AND status changed TO Done AND updatedDate > "{} 00:00" AND updatedDate < "{} 00:00" AND fixVersion = {}'
        JQL_command = template_of_JQL_command.format(project_name, start_date, end_date, version)
        JQQ = 'project = "OWA" AND issuetype in (Bug,Story) AND status changed TO Done AND updatedDate > "2020/04/01 00:00" AND updatedDate < "2020/04/20 00:00" AND fixVersion = 1.0.0'
        results = self.__jira_handler.search_issues(JQL_command, startAt=0, maxResults=200)
        tickets_found = len(results)
        return tickets_found

    def get_stories_and_bugs_from_backlog(self):
        pass

    def get_stories_and_bugs_from_board_that_are_in_progress(self):
        pass

    def get_tickets_that_do_not_have_story_points_and(self):
        pass

    def check_target_issue(self,issue, target_ticket:str):
        '''
        helper function to see the contents of a ticket
        :param issue: jira object
        :param target_ticket: e.g. 'OWA-1315'
        :return:
        '''
        ticket_name = str(issue.key)

        if ticket_name == target_ticket:
            fmt = json.dumps(issue.raw, indent=2)
            print('raw issue fields', fmt)

    def get_complex_time_estimation(self, issue):

        not_having_time_estimation = (issue.fields.timeoriginalestimate in (None, 0) ) ^ \
                                     (issue.fields.timeestimate in (None, 0)) #^ \
                                     # (issue.raw.fields.aggregatetimeestimate in (0))

        return not_having_time_estimation



    def get_stories_and_bugs_tickets_that_are_in_progress_for_a_specific_version(self, project_name: str = None, version: str = None):
        if version is None:
            version = self.__version

        if project_name is None:
            project_name = self.__project_name


        output = {'timestamp_this_was_created':self.get_now_as_a_string()}
        output['version'] = version
        output['where'] = 'Kanban Board'


        query = 'issuetype in (Bug, Story) AND project = '+project_name+' AND fixVersion = '+version+' AND resolution = Unresolved AND status in (Blocked, "Code Review", "In Development", "Preparing Tests", QA, "Selected for Development", UAT) ORDER BY priority DESC, updated DESC'
        results = self.__jira_handler.search_issues(query, startAt=0, maxResults=200)



        for issue in results:

            obj = {}
            ticket_name = str(issue.key)
            status = str(issue.fields.status)
            member_of_team = str(issue.fields.assignee)
            issue_type = str(issue.fields.issuetype).lower()


            not_having_time_estimation = (issue.fields.timeestimate in (None, 0))
            being_a_story_without_story_points = (issue.fields.customfield_10026 in (None,0) ) and (issue_type == 'story')


            if not_having_time_estimation == True :
                if member_of_team not in output.keys():
                    output[member_of_team] = {}
                if ticket_name not in output[member_of_team].keys():
                    output[member_of_team][ticket_name] = {}
                if 'column' not in output[member_of_team][ticket_name].keys():
                    output[member_of_team][ticket_name] = {'column': status}

                # print(issue.key, issue_type, 'no time estimate from', member_of_team)
                output[member_of_team][ticket_name] = {'time_estimation':'<---please time-estimate'}


            if being_a_story_without_story_points == True:
                if member_of_team not in output.keys():
                    output[member_of_team] = {}
                if ticket_name not in output[member_of_team].keys():
                    output[member_of_team][ticket_name] = {}
                if 'column' not in output[member_of_team][ticket_name].keys():
                    output[member_of_team][ticket_name] = {'column': status}
                # print(issue.key, issue_type,  'no story points from', member_of_team)
                output[member_of_team][ticket_name] = {'story points': '<---please estimate'}

        return output


    def print_short_message_for_update(self, input: dict):
        print('Updates required for ', input["where"], ', generated at',input["timestamp_this_was_created"], ":")

        for item in input.keys():
            if item not in ("timestamp_this_was_created", "version", "where"):
                print(item)
                for issue_name, ticket in input[item].items():
                    print("\t", issue_name, ticket)

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