import os
from datetime import datetime, timedelta
from typing import Any, Dict, Generator, List
from typing import Dict, Tuple, Sequence

import requests
# Optional - to connect using OAuth credentials
from oauthlib.oauth1 import SIGNATURE_RSA


class JiraClient:
    def __init__(
            self,
            username: str = None,
            api_token: str = None,
            access_token: str = None,
            access_token_secret: str = None,
            consumer_key: str = None,
            key_cert: str = None,
    ):
        self._user_url = os.getenv("JIRA_SERVER", "").rstrip("/")
        self._base_url = f"{self._user_url}/rest/api/3"

        if username and api_token:
            self._session = requests.Session()
            self._session.auth = (username, api_token)
            return
        elif access_token and access_token_secret and consumer_key and key_cert:
            self._session = OAuth1Session(
                consumer_key,
                rsa_key=key_cert,
                resource_owner_key=access_token,
                resource_owner_secret=access_token_secret,
                signature_method=SIGNATURE_RSA,
            )
        else:
            raise ValueError("Must use API token or OAuth credentials")

    def _get_paginated_results(
            self, url: str, results_key: str, parameters: Dict[str, Union[str, int]] = None, use_post: bool = False,
    ) -> Generator[Dict[str, Any], None, None]:
        """Get results of a paginated call that uses 'maxResults', 'startAt', and 'total' attributes.

        :param url: URL without any pagination parameters
        :param results_key: The key of the response dict that contains the actual elements to return (varies from calls to calls). Ex.: "items"
        :param parameters: If use_post is False, URL parameters. If use_post is True, json encoded body parameters
        :param use_post: Use POST instead of GET. Needed if parameters are too long to fit in an URL
        """
        parameters = parameters or {}

        results_per_page = RESULTS_PER_PAGE
        parameters["maxResults"] = results_per_page
        next = 0
        while True:
            parameters["startAt"] = next
            if use_post:
                response = self._session.post(url, json=parameters)
            else:
                response = self._session.get(url, params=parameters)
            response.raise_for_status()
            response_json = response.json()
            results = response_json[results_key]

            if response_json["maxResults"] < results_per_page:
                # Some calls limit the maximum value of maxResults
                results_per_page = response_json["maxResults"]
                parameters["maxResults"] = results_per_page

            for result in results:
                yield result

            next += results_per_page
            if next >= response_json["total"]:
                return

    def _get_paginated_results_with_next_page_link(self, url: str) -> Generator[Dict[str, Any], None, None]:
        """Get results of a call that returns a payload with the lastPage and nextPage attributes"""
        is_last_page = False
        while not is_last_page:
            response = self._session.get(url)
            response.raise_for_status()
            response_json = response.json()
            for result in response_json["values"]:
                yield result

            is_last_page = response_json.get("lastPage", True)
            if not is_last_page:
                url = response_json["nextPage"]

    def retrieve_worklogs_updated_since(self, start: datetime) -> List[Dict[str, Any]]:
        """Retrieve worklog objects for all worklogs that have been created or updated since the provided datetime

        Faster than getting worklogs through issues
        """
        worklog_ids: List[str] = []
        for worklog_entry in self._get_paginated_results_with_next_page_link(
                f"{self._base_url}/worklog/updated?since={int(start.timestamp() * 1000)}"
        ):
            worklog_ids.append(worklog_entry["worklogId"])

        worklogs_per_page = 1000
        ids_in_groups_per_page = [worklog_ids[i: i + worklogs_per_page] for i in
                                  range(0, len(worklog_ids), worklogs_per_page)]
        worklogs: List[Dict[str, Any]] = []
        # This is kind of a manual pagination. The documentation only states "The returned list of worklogs is limited to 1000 items."
        # Doc: https://developer.atlassian.com/cloud/jira/platform/rest/v3/#api-rest-api-3-worklog-list-post
        for ids_to_get in ids_in_groups_per_page:
            for worklog in self._session.post(f"{self._base_url}/worklog/list", json={"ids": ids_to_get}).json():
                # Optionnaly remove the worklogs you don't want (not in the right time period)
                worklogs.append(worklog)

        return worklogs

    def search_issues(self, jql: str, fields: List[str] = None) -> List[Dict[str, Any]]:
        """Return issues that matches a specified JQL query"""
        issues: List[Dict[str, Any]] = []
        parameters: Dict[str, Union[str, List[str]]] = {"jql": jql}
        if fields:
            parameters["fields"] = fields
        for issue in self._get_paginated_results(f"{self._base_url}/search", parameters=parameters,
                                                 results_key="issues", use_post=True):
            issues.append(issue)

        return issues

    # Point 3 - get issues for the retrieved worklogs
    def retrieve_issues_for_worklogs(self, worklogs: List[Dict[str, Any]], fields: List[str] = None) -> List[
        Dict[str, Any]]:
        """Get Issue objects referenced in a list of worklogs"""
        return self.search_issues(f"id in ({','.join(str(issue_id) for issue_id in set(worklog["
        issueId
        "] for worklog in worklogs))})", fields = fields)


        # Example usage
        os.environ["JIRA_SERVER"] = "https://mycompany.atlassian.net/"
        client = JiraClient("me@companyname.com", "my_api_token_12345")
        recent_worklogs = client.retrieve_worklogs_updated_since(datetime.now() - timedelta(days=14))