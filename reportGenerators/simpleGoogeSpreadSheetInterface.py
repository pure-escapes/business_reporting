#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


class simpleGoogleSpreadSheetGetter:
    __SCOPES = None
    __SAMPLE_SPREADSHEET_ID = None
    __SAMPLE_RANGE_NAME = None
    __google_credentials = None
    __expected_files = []
    __authorised_google_sheet = None

    def __init__(self, path_to_reports_configuration):

        with open(path_to_reports_configuration, "r") as spread_sheet_config:
            data = json.load(spread_sheet_config)
            self.__SCOPES = data["SCOPES"]
            self.__SAMPLE_SPREADSHEET_ID = data["SAMPLE_SPREADSHEET_ID"]
            self.__SAMPLE_RANGE_NAME = data["SAMPLE_RANGE_NAME"]

            path_to_googlecredentials = data["path_to_google_credentials"]
            if not os.path.exists(path_to_googlecredentials):
                raise OSError(1, 'could not find file %s' % path_to_googlecredentials)






        self.__google_credentials = ServiceAccountCredentials.from_json_keyfile_name('quickstart-1587116956725-0e4af7534e06.json')
        self.__authorised_google_sheet = None


    def get_values_from_spreadsheet(self):

        wks = gc.open("test_report45").sheet1
        gc = gspread.authorize(self.__google_credentials)

        service = build('sheets', 'v4', credentials=self.__google_credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.__SAMPLE_SPREADSHEET_ID,
                                    range=self.__SAMPLE_RANGE_NAME).execute()
        values_from_spreadsheet = result.get('values', [])

        return values_from_spreadsheet

    def show_data(self):
        values_from_spreadsheet = self.get_values_from_spreadsheet()

        if not values_from_spreadsheet:
            print('No data found.')
        else:
            print('data I read:')
            for row in values_from_spreadsheet:
                print(row)