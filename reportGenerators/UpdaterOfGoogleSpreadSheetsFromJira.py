#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import json

class UpdaterOfGoogleSpreadSheetsFromJira:
    __output = {}
    __configuration = None
    __additional_files_to_consider = []


    def __init__(self, configuration, additional_files_to_consider=[]):
        self.__configuration = configuration
        self.__additional_files_to_consider = additional_files_to_consider

    def calculate_team_velocity(self):
        velocity_of_this_period = self.__configuration["input"]["at_the_end_of_the_period"]["tickets_completed"]
        number_additional_files = len(self.__additional_files_to_consider)
        if number_additional_files == 0:
            self.__configuration["calculated"]["team_velocity"] = velocity_of_this_period
        else:
            temp_velocity_from_additional_files = 0
            for configuration in self.__additional_files_to_consider:
                with open(configuration, 'r') as input_file:
                    temp_configuration = json.load(input_file)
                    temp_velocity_from_additional_files += temp_configuration["input"]["at_the_end_of_the_period"]["tickets_completed"]

            calculated_velocity = (temp_velocity_from_additional_files + velocity_of_this_period)/number_additional_files
            self.__configuration["calculated"].update( team_velocity = calculated_velocity )
            # self.__configuration["calculated"]["team_velocity"] = (temp_velocity_from_additional_files + velocity_of_this_period)/number_additional_files



    def calculate_estimation_to_completion(self):
        C3 = self.__configuration["input"]["at_the_start_of_the_period"]["backlog_size"]
        C7 = self.__configuration["input"]["at_the_end_of_the_period"]["tickets_added_to_backlog_during_the_period"]
        C8 = self.__configuration["input"]["at_the_end_of_the_period"]["bugs_added_to_backlog_during_the_period"]

        C5 = self.__configuration["input"]["at_the_end_of_the_period"]["tickets_completed"]
        C9 = self.__configuration["input"]["at_the_end_of_the_period"]["tickets_removed_from_backlog_during_the_period"]

        self.__configuration["calculated"].update( estimated_days_to_complete = ( (C3+C7+C8) - (C5+C9) ) / self.__configuration["calculated"]["team_velocity"] )




    def calculate_weighted_iterations_to_completion(self):
        result = (self.__configuration["calculated"]["estimated_days_to_complete"] *100) / (100 - self.__configuration["input"]["at_the_start_of_the_period"]["capacity_ratio_for_bugs"] )
        result = round(result, 2)
        self.__configuration["calculated"].update( weighted_iterations_to_complete=result)


    def calculate_relative_difference(self):
        A = self.__configuration["calculated"]["estimated_days_to_complete"]
        B = self.__configuration["calculated"]["weighted_iterations_to_complete"]
        result = ((B - A) * 100) / A
        result = round (result, 2)
        self.__configuration["calculated"].update(relative_difference_between_estimation_and_weighted_iterations=result )


    def update(self):
        status = False
        return status

    def calculate(self):
        self.calculate_team_velocity()
        self.calculate_estimation_to_completion()
        self.calculate_weighted_iterations_to_completion()
        self.calculate_relative_difference()

        return self.__configuration["calculated"]