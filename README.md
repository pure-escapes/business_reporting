# business_reporting
generate analytics for reporting purposes




# pre-requisites before running
1. use the correct google account
1. google API needs to be enabled ( from https://developers.google.com/sheets/api/quickstart/python/?authuser=4 )
    1. if this had happened before, check permissions of tokens at https://console.developers.google.com/apis/credentials
    1. also google drive API (not just the spreadsheets)
1. the file `credentials.json` must exist in the directory where the script will run
1. the target spreadsheet exists on google drive
1. for service accounts, the target spreadsheet needs to be shared with that account, too

# installation of scripts

After creating a pipenv 

```bash
pipenv install
```

# test
after activating  the virtual environment and having created any files required
```bash
pipenv run pytest
```

# execution steps for an example (test_report45)

1. a file called `test_report45` was created on google drive *with some* data in the first few cells
1. the ID of the file was captured from the browser and was inserted into the configuration file `spread_sheet_specifics_for_test_report45.json` 