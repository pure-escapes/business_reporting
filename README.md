# business_reporting
generate analytics for reporting purposes




# pre-requisites before running
1. use the correct google account
1. google API needs to be enabled ( from https://developers.google.com/sheets/api/quickstart/python/?authuser=4 )
    1. if this had happened before, check permissions of tokens at https://console.developers.google.com/apis/credentials
1. the file `credentials.json` must exist in the directory where the script will run
1. the target spreadsheet exists on googledrive

# installation

After creating a pipenv 

```bash
pipenv install
```

# execution steps for an example (test_report45)

1. a file called `test_report45` was created on google drive
1. the ID of the file was captured from the browser and was inserted into the configuration file `spread_sheet_specifics_for_test_report45.json` 