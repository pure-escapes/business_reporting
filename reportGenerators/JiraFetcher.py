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

        self.__where = {'board': 'Blocked, "Code Review", "In Development", "Preparing Tests", QA, "Selected for Development", UAT',
                        'backlog': 'Backlog'}

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

    def get_quality_from_the_main_board_for_a_specific_version(self, project_name: str = None, version: str = None):
        where_option = 'board'
        return self.get_quality_for_a_specific_version(where_option, project_name, version)

    def get_quality_from_backlog_for_a_specific_version(self, project_name: str = None, version: str = None):
        where_option = 'backlog'
        return self.get_quality_for_a_specific_version(where_option, project_name, version)

    def get_quality_of_multiple_versions(self, project_name: str, assessment_by_versions: dict):
        '''

        :param project_name: e.g. 'OWA'
        :param assessment_by_versions: e.g. {
                            "1.1.0":{},
                            "1.2.0":{},
                            "1.3.0":{},
                            "2.0.0":{}
                            }
        :return:
        '''
        for version in assessment_by_versions.keys():
            # print('checking version', version)
            report_object = self.get_quality_from_backlog_for_a_specific_version(
                project_name=project_name, version=version)

            print('version', version, ', failure rate:',report_object['calculations']['failure_rate']*100)
            assessment_by_versions[version] = report_object


    def get_quality_for_a_specific_version(self, where_option: str, project_name: str = None, version: str = None):
        if version is None:
            version = self.__version

        if project_name is None:
            project_name = self.__project_name


        output = {'timestamp_this_was_created':self.get_now_as_a_string()}
        output['version'] = version

        if where_option == 'board':
            output['where'] = 'Kanban Board'
        else:
            output['where'] = '(just the) Backlog'

        output['feature'] = []
        output['maintenance'] = []
        output['rework'] = []
        output['defect'] = []
        output['unclassified'] = []
        output['statistics'] = {"number_of_features": 0,
                                "number_of_maintenance": 0,
                                "number_of_rework": 0,
                                "number_of_calculations": 0,
                                "number_of_unclassified": 0}
        output['calculations'] = {"value_supply": 0,
                                  "failure_supply": 0,
                                  "total_number_of_items": 0,
                                  "failure_rate": 0}

        columns_to_query = self.__where[where_option]

        query = 'issuetype in (Bug, Story) AND project = '+project_name+' AND fixVersion = '+version+' AND resolution = Unresolved AND status in ('+columns_to_query+') ORDER BY priority DESC, updated DESC'
        results = self.__jira_handler.search_issues(query, startAt=0, maxResults=200)



        for issue in results:

            obj = {}
            ticket_name = str(issue.key)
            status = str(issue.fields.status)
            member_of_team = str(issue.fields.assignee)
            jira_issue_type = str(issue.fields.issuetype).lower()
            item_type = str(issue.fields.customfield_10037).lower()

            if item_type == 'feature':
                output['feature'].append(ticket_name)
            if item_type == 'maintenance':
                output['maintenance'].append(ticket_name)
            if item_type == 'rework':
                output['rework'].append(ticket_name)
            if item_type == 'defect':
                output['defect'].append(ticket_name)
            if item_type not in ('feature', 'maintenance', 'rework', 'defect'):
                output['unclassified'].append(ticket_name)



        number_of_features = len(output['feature'])
        number_of_maintenance = len(output['maintenance'])
        number_of_rework = len(output['rework'])
        number_of_defect = len(output['defect'])
        number_of_unclassified = len(output['unclassified'])
        output['statistics']["number_of_features"] = number_of_features
        output['statistics']["number_of_maintenance"] = number_of_maintenance
        output['statistics']["number_of_rework"] = number_of_rework
        output['statistics']["number_of_calculations"] = number_of_defect
        output['statistics']["number_of_unclassified"] = number_of_unclassified

        value_supply = number_of_features + number_of_maintenance
        failure_supply = number_of_rework + number_of_defect
        total_number_of_items = value_supply + failure_supply

        if total_number_of_items == 0:
            output['calculations']["value_supply"] = 0
            output['calculations']["failure_supply"] = 0
            output['calculations']["total_number_of_items"] = total_number_of_items
            output['calculations']["failure_rate"] = 1

        else:
            failure_rate = 1.0 * failure_supply / total_number_of_items
            output['calculations']["value_supply"] = value_supply
            output['calculations']["failure_supply"] = failure_supply
            output['calculations']["total_number_of_items"] = total_number_of_items
            output['calculations']["failure_rate"] = failure_rate






        return output

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

    def print_short_message_for_quality_assessment(self, input: dict, toggle_for_PS = True):
        print('Agile Quality assessment (via Jira) of ', input["where"], ' for version ', input["version"], ', generated at',input["timestamp_this_was_created"], ":")
        total_number_of_items = input['calculations']['total_number_of_items']
        number_of_unclassified_items = input['statistics']['number_of_unclassified']
        unclassified_tickets = input['unclassified']
        failure_rate = input['calculations']['failure_rate']


        print('total tickets:', str(total_number_of_items))
        if number_of_unclassified_items != 0:
            unclassified_tickets.sort()
            print('\tBUT, ', str(number_of_unclassified_items), 'more tickets are unclassified! (i.e., ', ", ".join(unclassified_tickets), ')')
        print("with failure_rate:", str(round(failure_rate*100, 2)), "% (ideally, as low as possible)")

        if toggle_for_PS == True :
            print("\n")
            print('\tPS1: more info about "how to read this?" at https://pureescapes.atlassian.net/wiki/spaces/PEOWA/pages/309493777/Refining+the+Agile+process#Assessing-versions-%26-backlog')
            print('\tPS2: the unclassified tickets are not considered in the calculations')


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