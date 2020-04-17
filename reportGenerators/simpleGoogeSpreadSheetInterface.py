#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import gspread
import json
import os

from oauth2client.service_account import ServiceAccountCredentials

class simpleGoogleSpreadSheetGetter:
    __SCOPES = None
    __SAMPLE_SPREADSHEET_ID = None
    __SAMPLE_RANGE_NAME = None
    __google_credentials = None
    __expected_files = []
    __authorised_access_to_google_spreadsheet = None
    __name_of_google_spreadsheet = None

    def __init__(self, path_to_reports_configuration):

        with open(path_to_reports_configuration, "r") as spread_sheet_config:
            data = json.load(spread_sheet_config)
            self.__SCOPES = data["SCOPES"]
            self.__SAMPLE_SPREADSHEET_ID = data["SAMPLE_SPREADSHEET_ID"]
            self.__SAMPLE_RANGE_NAME = data["SAMPLE_RANGE_NAME"]

            self.__path_to_google_credentials = data["path_to_google_credentials"]
            if not os.path.exists(self.__path_to_google_credentials):
                raise OSError(1, 'could not find file %s' % self.__path_to_google_credentials)
            else:

                self.__name_of_google_spreadsheet = data["name_of_spreadsheet_on_google_drive"]



        self.__google_credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__path_to_google_credentials, self.__SCOPES)
        self.__authorised_access_to_google_spreadsheet = gspread.authorize(self.__google_credentials)


    def get_values_from_spreadsheet(self):
        wks = self.__authorised_access_to_google_spreadsheet.open(self.__name_of_google_spreadsheet)
        values_from_spreadsheet = wks.sheet1.get_all_records()
        print(values_from_spreadsheet)
        return values_from_spreadsheet

    def show_data(self):
        values_from_spreadsheet = self.get_values_from_spreadsheet()

        if not values_from_spreadsheet:
            print('No data found.')
        else:
            print('data I read:')
            for row in values_from_spreadsheet:
                print(row)

    def change_something(self):
        wks = self.__authorised_access_to_google_spreadsheet.open(self.__name_of_google_spreadsheet)
        wks.sheet1.update_acell('A1','my new text')