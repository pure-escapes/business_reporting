from flask import Flask, render_template, request, redirect, url_for, flash, g, jsonify
import json
import os.path

import sqlite3

import reportGenerators.weekly_reporting as WR
import datetime


app = Flask(__name__)
app.secret_key = 'h2h2h2hohihihih2222442'


weeks = {
    28:{
        'start_date': datetime.datetime(2020, 7, 6, 0, 0, 1),
        'end_date': datetime.datetime(2020, 7, 10, 23, 59, 59)
    },
    29:{
            'start_date': datetime.datetime(2020, 7, 13, 0, 0, 1),
            'end_date': datetime.datetime(2020, 7, 17, 23, 59, 59)
        },
    30:{
            'start_date': datetime.datetime(2020, 7, 20, 0, 0, 1),
            'end_date': datetime.datetime(2020, 7, 24, 23, 59, 59)
        },
    31:{
            'start_date': datetime.datetime(2020, 7, 27, 0, 0, 1),
            'end_date': datetime.datetime(2020, 7, 31, 23, 59, 59)
        },
    32:{
            'start_date': datetime.datetime(2020, 8, 3, 0, 0, 1),
            'end_date': datetime.datetime(2020, 8, 7, 23, 59, 59)
        },
    33:{
            'start_date': datetime.datetime(2020, 8, 10, 0, 0, 1),
            'end_date': datetime.datetime(2020, 8, 14, 23, 59, 59)
        },
    34:{
            'start_date': datetime.datetime(2020, 8, 17, 0, 0, 1),
            'end_date': datetime.datetime(2020, 8, 21, 23, 59, 59)
        }
}




@app.route('/week/<int:week_selector>')
def generate_report_for_week(week_selector: int):
    target_versions = ["1.0.0", "1.1.0", "1.2.0"]
    start_date = weeks[week_selector]['start_date']
    end_date = weeks[week_selector]['end_date']
    return WR.generate_all_reporting_data_for_specific_week(target_versions, start_date, end_date)


@app.errorhandler(404)
def page_not_found(error):
    return 'Non existing functionality in business reporting', 404


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0')
