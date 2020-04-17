# business_reporting
generate analytics for reporting purposes


# GoogleSheet & Google drive



references: 
- gspread github
- https://developers.google.com/sheets/api/quickstart/python/?authuser=4

## pre-requisites before running
1. use the correct google account
1. google Sheets API needs to be enabled ( from https://developers.google.com/sheets/api/quickstart/python/?authuser=4 )
    1. if this had happened before, check permissions of tokens at https://console.developers.google.com/apis/credentials
1. google drive API (not just the spreadsheets) needs to be enabled
1. credentials needs to be created
    1. the file `credentials.json` must exist in the directory where the script will run
1. the target spreadsheet exists on google drive
1. for service accounts, the target spreadsheet needs to be shared with that account, too

## installation of scripts

After creating a pipenv 

```bash
pipenv install
```

## test
after activating  the virtual environment and having created any files required
```bash
pipenv run pytest
```

## execution steps for an example (test_report45)

1. a file called `test_report45` was created on google drive *with some* data in the first few cells
1. the ID of the file was captured from the browser and was inserted into the configuration file `spread_sheet_specifics_for_test_report45.json`


# Jira

references: https://jira.readthedocs.io/en/master/examples.html
https://developer.atlassian.com/cloud/jira/software/getting-started/

# preparation

create environment variables
 - `PE_JIRA_USERNAME` and `PE_JIRA_PASSWORD` with the appropriate values;
 - create API token named as `PE_JIRA_BI_LISTENER` from https://id.atlassian.com/manage-profile/security/api-tokens
 - `PE_JIRA_URI` with PE's jira details
 
 The following should be working:
 ```bash
curl -v $PE_JIRA_URI --user $PE_JIRA_USERNAME:$PE_JIRA_BI_LISTENER
```

