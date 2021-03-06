#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) Pure Escapes 2020 - All Rights Reserved
Unauthorized copying of this file, via any medium is strictly prohibited
Proprietary and confidential

Written by Christos Tsotskas <info@pure-escapes.com>, April 2020

"""

from __future__ import print_function
import pickle
import os.path
import json
import os


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class NativeGoogleSpreadSheetGetter:
    __SCOPES = None
    __SAMPLE_SPREADSHEET_ID = None
    __SAMPLE_RANGE_NAME = None
    __google_credentials = None
    __expected_files = []
    __path_to_google_credentials = None

    def __init__(self, path_to_reports_configuration):

        with open(path_to_reports_configuration, "r") as spread_sheet_config:
            data = json.load(spread_sheet_config)
            self.__SCOPES = data["SCOPES"]
            self.__SAMPLE_SPREADSHEET_ID = data["SAMPLE_SPREADSHEET_ID"]
            self.__SAMPLE_RANGE_NAME = data["SAMPLE_RANGE_NAME"]


            if not os.path.exists(data["path_to_google_credentials"]):
                raise OSError(1, 'could not find file %s' % self.__path_to_google_credentials)
            else:
                self.__path_to_google_credentials = data["path_to_google_credentials"]

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.__google_credentials = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.__google_credentials or not self.__google_credentials.valid:
            if self.__google_credentials and self.__google_credentials.expired and self.__google_credentials.refresh_token:
                self.__google_credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.__path_to_google_credentials, self.__SCOPES)
                self.__google_credentials = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.__google_credentials, token)

    def get_values_from_spreadsheet(self):

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

