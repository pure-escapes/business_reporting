

import unittest
import os
import json
import requests

import dateutil
from dateutil.parser import parse
import datetime

class CircleCI_Fetcher():

    def __init__(self):
        pass



    def get_now_as_a_string(self):
        now_time_object = datetime.datetime.now()
        return now_time_object.strftime("%Y%m%d_%H%M")


    def get_deployments_of_a_branch_within_a_specific_range_of_dates(self, config: dict, minimal_print = True):
        '''

        :param config: dictionary such as:

            {"start_date_as_str":"1/4/2020",
            "end_date_as_str":"29/4/2020",
            "circleCI_project":"webapp-backend",
            "name_of_job_that_deploys_to_production":"deploy_sandbox",
            "name_of_github_branch_related_to_production":"sandbox"}

        :param minimal_print: boolean toggle that activates a basic print statement after the calculation

        '''
        start_date_as_str = config["start_date_as_str"]
        end_date_as_str = config["end_date_as_str"]
        circleCI_project = config["circleCI_project"]
        name_of_job_that_deploys_to_production = config["name_of_job_that_deploys_to_production"]
        name_of_github_branch_related_to_production = config["name_of_github_branch_related_to_production"]

        from_selected_year = parse(start_date_as_str).year
        from_selected_month = parse(start_date_as_str).month
        from_selected_day = parse(start_date_as_str).day


        to_selected_year = parse(end_date_as_str).year
        to_selected_month = parse(end_date_as_str).month
        to_selected_day = parse(end_date_as_str).day

        start_date = (from_selected_day, from_selected_month, from_selected_year)

        end_date = (to_selected_day, to_selected_month, to_selected_year)


        token_value = os.environ.get('PE_CIRCLECI_API_TOKEN')
        headers = {
            'Circle-Token': token_value,
        }

        params = (
            ('branch', name_of_github_branch_related_to_production),
        )

        URL = 'https://circleci.com/api/v2/insights/gh/pure-escapes/'+circleCI_project+'/workflows/build-and-deploy/jobs/'+name_of_job_that_deploys_to_production
        response = requests.get(URL,headers=headers, params=params)

        # NB. Original query string below. It seems impossible to parse and
        # reproduce query strings 100% accurately so the one below is given
        # in case the reproduced version is not "correct".
        # response = requests.get('https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs/deploy_sandbox?branch=sandbox', headers=headers)


        # print(response.text)
        #todo: consider pagination in the results
        # todo use PycURL instead of `requests`

        data_to_parse = response.json()['items']

        counter_of_jobs = 0
        counter_of_successful_jobs = 0
        for job in data_to_parse:
            date = parse(job["started_at"])

            current_date = (date.day, date.month, date.year)


            if (job["status"] == "success") and (start_date < current_date < end_date):
                # print(job['id'], date.date(), date.month, date.year)
                counter_of_successful_jobs += 1
            counter_of_jobs += 1
        if counter_of_jobs != 0:
            efficiency = round(100.0 * counter_of_successful_jobs / counter_of_jobs, 2)
        else:
            efficiency = 0.0

        if minimal_print == True:
            print(circleCI_project, " between",start_date_as_str ,"and", end_date_as_str,', total deployments(i.e., CircleCI jobs) to production (i.e., sandbox):', counter_of_jobs, "(", efficiency ,"% successful)")

        return counter_of_successful_jobs, efficiency, counter_of_jobs

    def check_several_branches(self, config):
        output = config
        output['timestamp_this_was_created'] = self.get_now_as_a_string()

        for job in config["projects"].keys():

            temp_dict = {}
            temp_dict["start_date_as_str"] = config["start_date_as_str"]
            temp_dict["end_date_as_str"] = config["end_date_as_str"]
            temp_dict["circleCI_project"] = job
            temp_dict["name_of_job_that_deploys_to_production"] = config["projects"][job]["name_of_job_that_deploys_to_production"]
            temp_dict["name_of_github_branch_related_to_production"] = config["projects"][job]["name_of_github_branch_related_to_production"]


            counter_of_successful_jobs, efficiency, counter_of_jobs = self.get_deployments_of_a_branch_within_a_specific_range_of_dates(temp_dict, minimal_print=False)
            output["projects"][job]["calculated"]["number_of_successful_deployments"] = counter_of_successful_jobs
            output["projects"][job]["calculated"]["efficiency"] = efficiency
            output["projects"][job]["calculated"]["total_number_of_deployments"] = counter_of_jobs


        return output


    def show(self, input: dict):

        start_date_as_str = input["start_date_as_str"]
        end_date_as_str = input["end_date_as_str"]
        print('DevOps Quality assessment (via CircleCI) between', start_date_as_str, 'and', end_date_as_str ,', generated at', input["timestamp_this_was_created"], ":")


        for job in input["projects"].keys():
            circleCI_project = job
            counter_of_jobs = input["projects"][job]["calculated"]["total_number_of_deployments"]
            efficiency = input["projects"][job]["calculated"]["efficiency"]
            print("\t", circleCI_project, " between", start_date_as_str, "and", end_date_as_str,
                  ', total deployments(i.e., CircleCI jobs) to production (i.e., sandbox):', counter_of_jobs, "(",
                  efficiency, "% successful)")