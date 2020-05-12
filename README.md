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

# CircleCI:

## preparation
1. get a token from the site, from personal tokens, add to your env variables (e.g., as `PE_CIRCLECI_API_TOKEN`)
1. check that it works
```bash
curl https://circleci.com/api/v2/me --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

### utilities

an example of `slug`
```html
gh/pure-escapes/webapp-backend
```


project info
```bash
curl https://circleci.com/api/v2/project/gh/pure-escapes/webapp-backend --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

example of workflow metrics
```html
curl -X GET https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows  --header 'Content-Type: application/json' --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

getting jobs of a particular workflow
```html
curl -X GET https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs  --header 'Content-Type: application/json' --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

getting job statistics from job `deploy_develop`
```html
curl -X GET https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs/deploy_develop --header 'Content-Type: application/json' -header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

getting all jobs from a specific workflow `build_and_deploy`
```html
curl -X GET https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-frontend/workflows/build_and_deploy --header 'Content-Type: application/json' --header "Circle-Toen: $PE_CIRCLECI_API_TOKEN"
```

getting job details for a specific job number
```html
curl -X GET https://circleci.com/api/v2/project/gh/pure-escapes/webapp-frontend/job/706 --header 'Content-Type: application/json' --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```

getting the status of specific job for a specific branch
```html
curl -X GET https://circleci.com/api/v2/insights/gh/pure-escapes/webapp-backend/workflows/build-and-deploy/jobs/deploy_sandbox?branch=sandbox --header "Circle-Token: $PE_CIRCLECI_API_TOKEN"
```



## references

https://circleci.com/docs/api/v2/#circleci-api 
https://circleci.com/docs/2.0/api-developers-guide/#section=reference
https://circleci.com/docs/2.0/api-intro/#section=reference
https://circleci.com/docs/

# Usage




# Future Work

1. use data from CircleCI https://circleci.com/blog/announcing-circleci-s-100m-series-e/ (count Deployments per day)
1. create reports on jupyter notebook and automatically share
1. use analytics from sonarcloud
1. use analytics from github
1. from analytics, get all tickets currently on kanban that need updating for version numbers. story points (if not a bug) and time estimations 
1. check if tickets from backlog are ready to go to the kanbanboard!
1. check priorities of certain tickets
1. set priorities to specific tickets
1. check weekly how many hours of work have been logged, and against which tickets
1. calculate averages over a specific period (and include versions)
1. find unassigned tickets, too!
1. check the 'completeness' of a list of tickets
```bash
issueKey in (OWA-1462,OWA-1372,OWA-661,OWA-666,OWA-1283,OWA-1504,OWA-959,OWA-1505,BAU-8,BAU-9,BAU-10,OWA-1496,OWA-1501,OWA-1267,OWA-1493,BAU-33,BAU-36,OWA-1293,BAU-46,OWA-1034,BAU-52,OWA-1315,OWA-1317,OWA-1334,OWA-1339,OWA-1362,OWA-1365,OWA-1499,OWA-1369,OWA-1374,OWA-1375,OWA-1376,OWA-1500,BAU-71,BAU-73,OWA-1397,OWA-1402,OWA-1426,OWA-1427,OWA-1428,OWA-1429,OWA-1431,OWA-1432,OWA-1434,OWA-1451,OWA-1453,OWA-1455,OWA-1458,OWA-1481,OWA-1482)
```
1. use analytics from CircleCI to get deployments
1. in the quality assessment of backlog & kanban, the tasks should be included (and considered something separate)