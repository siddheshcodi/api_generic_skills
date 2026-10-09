"""Jira adapter (Cloud and Data Center/Server) using REST API v2 (wiki-markup descriptions).
Cloud auth: email + API token (Basic). Data Center: Personal Access Token (Bearer).
Search: Cloud uses /rest/api/2/search/jql (old /search was removed in 2025); DC uses /rest/api/2/search."""
import base64
import re
import urllib.parse

from .common import (DUPLICATE_THRESHOLD, Tracker, TrackerError, env_value, http_json, map_custom_fields,
                     similarity)

_JQL_SPECIAL = re.compile(r'[+\-&|!(){}\[\]^~*?\\/:"\']')


class Jira(Tracker):
    name = "jira"
    description_format = "jira_wiki"

    @property
    def cloud(self):
        return (self.s.get("deployment") or "cloud").lower() == "cloud"

    def _base(self):
        url = (self.s.get("base_url") or "").rstrip("/")
        if not url or "yourcompany" in url:
            raise TrackerError("Set jira.base_url, e.g. https://yourcompany.atlassian.net")
        return url

    def _headers(self):
        token = env_value(self.s.get("api_token_env", "JIRA_API_TOKEN"), "Jira API token / PAT")
        if self.cloud:
            email = env_value(self.s.get("email_env", "JIRA_EMAIL"), "Jira account email")
            return {"Authorization": "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()}
        return {"Authorization": f"Bearer {token}"}

    def _call(self, method, path, body=None, params=None):
        url = self._base() + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        return http_json(method, url, self._headers(), body)

    def config_problems(self):
        return [f"jira.{k} is not set" for k in ("base_url", "project_key") if not self.s.get(k)]

    def target(self):
        return f"Jira {self.s.get('base_url')} -> project {self.s.get('project_key')} (issue type {self.s.get('issue_type', 'Bug')})"

    def build_payload(self, bug):
        f = {"project": {"key": self.s["project_key"]},
             "issuetype": {"name": self.s.get("issue_type") or "Bug"},
             "summary": self.title(bug)[:250],
             "description": self.description(bug)}
        prio = (self.s.get("severity_to_priority") or {}).get(bug["severity"])
        if prio:
            f["priority"] = {"name": prio}
        labels = [re.sub(r"\s+", "-", str(x)) for x in (self.s.get("labels") or []) if x]
        if self.s.get("add_severity_label", True):
            labels.append(f"severity-{bug['severity'].lower()}")
        if labels:
            f["labels"] = labels
        if self.s.get("components"):
            f["components"] = [{"name": c} for c in self.s["components"]]
        if self.s.get("default_assignee"):
            f["assignee"] = {"accountId": self.s["default_assignee"]} if self.cloud else {"name": self.s["default_assignee"]}
        if self.s.get("parent_key"):
            f["parent"] = {"key": self.s["parent_key"]}
        f.update(map_custom_fields(self.s.get("custom_fields"), bug))
        return {"fields": f}

    def preview_fields(self, p):
        f = p["fields"]
        rows = [("Summary", f["summary"]), ("Issue type", f["issuetype"]["name"]),
                ("Priority", (f.get("priority") or {}).get("name", "(project default)")),
                ("Labels", f.get("labels", [])), ("Assignee", f.get("assignee", "(unassigned)"))]
        extra = {k: v for k, v in f.items() if k.startswith("customfield_") or k in ("components", "parent")}
        if extra:
            rows.append(("Other fields", extra))
        return rows

    def preview_description(self, p):
        return p["fields"]["description"]

    def find_duplicates(self, title):
        words = _JQL_SPECIAL.sub(" ", re.sub(r"^\s*(\[[^\]]*\]\s*)+", "", title)).split()
        text = " ".join(words[:12])
        jql = (f'project = "{self.s["project_key"]}" AND issuetype = "{self.s.get("issue_type") or "Bug"}" '
               f'AND statusCategory != Done' + (f' AND summary ~ "{text}"' if text else ""))
        path = "/rest/api/2/search/jql" if self.cloud else "/rest/api/2/search"
        _, data = self._call("GET", path, params={"jql": jql, "fields": "summary,status", "maxResults": 50})
        hits = []
        for issue in (data or {}).get("issues", []):
            summary = (issue.get("fields") or {}).get("summary", "")
            sim = similarity(title, summary)
            if sim >= DUPLICATE_THRESHOLD:
                hits.append({"key": issue.get("key"), "title": summary,
                             "url": f"{self._base()}/browse/{issue.get('key')}", "similarity": sim})
        return hits

    def create(self, payload):
        _, data = self._call("POST", "/rest/api/2/issue", payload)
        if not isinstance(data, dict) or not data.get("key"):
            raise TrackerError(f"Jira did not return an issue key: {str(data)[:400]}")
        return {"id": data.get("id"), "key": data["key"], "url": f"{self._base()}/browse/{data['key']}"}

    def doctor(self):
        _, me = self._call("GET", "/rest/api/2/myself")
        _, proj = self._call("GET", f"/rest/api/2/project/{self.s['project_key']}")
        types = [t.get("name") for t in (proj or {}).get("issueTypes", [])]
        lines = [f"Logged in as: {(me or {}).get('displayName')} ({'Cloud' if self.cloud else 'Data Center'})",
                 f"Project: {(proj or {}).get('name')} [{self.s['project_key']}]"]
        wanted = self.s.get("issue_type") or "Bug"
        if types and wanted not in types:
            raise TrackerError(f"Issue type '{wanted}' not in project. Available: {types}")
        return lines

    def lookups(self):
        def projects(a):
            return [(p.get("key"), p.get("name")) for p in self._call("GET", "/rest/api/2/project")[1] or []]

        def issue_types(a):
            key = a.project or self.s.get("project_key")
            _, proj = self._call("GET", f"/rest/api/2/project/{key}")
            return [(t.get("id"), t.get("name")) for t in (proj or {}).get("issueTypes", [])]

        def priorities(a):
            return [(p.get("id"), p.get("name")) for p in self._call("GET", "/rest/api/2/priority")[1] or []]

        def users(a):
            if not a.query:
                raise TrackerError("Pass --query <name or email>")
            params = {"query": a.query} if self.cloud else {"username": a.query}
            data = self._call("GET", "/rest/api/2/user/search", params=params)[1] or []
            return [(u.get("accountId") or u.get("name"), f"{u.get('displayName')} {u.get('emailAddress', '')}") for u in data]

        def fields(a):
            data = self._call("GET", "/rest/api/2/field")[1] or []
            return [(x.get("id"), x.get("name")) for x in data if x.get("custom")]

        return {"projects": ("projects -> project_key", projects),
                "issue-types": ("issue types of --project", issue_types),
                "priorities": ("priority names -> severity_to_priority", priorities),
                "users": ("find user --query -> default_assignee", users),
                "fields": ("custom fields -> custom_fields ids", fields)}
