# Tracker: Jira (Cloud and Data Center / Server)

Set `bug_tracker.type: jira`. Common rules: `../bug-tracker-integration.md`.
Uses Jira REST API v2 (works on Cloud and Data Center; descriptions in wiki markup).

## Config
```yaml
jira:
  base_url: "https://yourcompany.atlassian.net"   # DC: https://jira.yourcompany.com
  deployment: cloud            # cloud | datacenter
  email_env: "JIRA_EMAIL"      # cloud only: your Atlassian account email
  api_token_env: "JIRA_API_TOKEN"   # cloud: API token; datacenter: Personal Access Token
  project_key: "QA"
  issue_type: "Bug"
  severity_to_priority: {Critical: Highest, High: High, Medium: Medium, Low: Low}
  labels: ["api-testing"]      # no spaces; "severity-<level>" is added automatically
  add_severity_label: true
  components: []               # component names, optional
  default_assignee: ""         # cloud: accountId; datacenter: username. Empty = unassigned
  parent_key: ""               # optional epic/parent issue key (team-managed projects)
  custom_fields: {}            # see below
```

## Credentials
- **Cloud:** create an API token at id.atlassian.com → Security → API tokens. Set
  `JIRA_EMAIL` and `JIRA_API_TOKEN`. Auth is Basic (email:token).
- **Data Center/Server:** Profile → Personal Access Tokens → create. Set `JIRA_API_TOKEN`.
  Auth is `Authorization: Bearer <PAT>`. `email_env` is ignored.

## Find values
```
python <skill>/scripts/bug_tracker.py lookup projects                 # → project_key
python <skill>/scripts/bug_tracker.py lookup issue-types --project QA # is "Bug" available?
python <skill>/scripts/bug_tracker.py lookup priorities               # → severity_to_priority names
python <skill>/scripts/bug_tracker.py lookup users --query "asha"     # → default_assignee
python <skill>/scripts/bug_tracker.py lookup fields                   # → custom field ids
python <skill>/scripts/bug_tracker.py doctor
```

## Custom fields
Map a bug value into a Jira custom field. Value format depends on field type:
```yaml
custom_fields:
  customfield_10050:              # text field → plain string
    from: environment
  customfield_10060:              # single-select → {"value": "<option>"}
    from: severity
    values:
      Critical: {value: "S1"}
      High: {value: "S2"}
      Medium: {value: "S3"}
      Low: {value: "S4"}
```
If a required field on the Bug screen isn't set, Jira returns 400 naming the field — add it here.

## Duplicate check
JQL: `project = KEY AND issuetype = Bug AND statusCategory != Done AND summary ~ "<words>"`,
then titles are compared for similarity. Cloud uses `/rest/api/2/search/jql` (the old
`/rest/api/2/search` was removed on Cloud in 2025); Data Center uses `/rest/api/2/search`.

## Troubleshooting
| Error | Fix |
|---|---|
| 401 | Cloud: wrong email or token; DC: wrong/expired PAT; check `deployment` value |
| 400 "priority ... cannot be set" | Priority field not on the Bug create screen — remove `severity_to_priority` or ask Jira admin |
| 400 "Field ... is required" | Add that field under `custom_fields` |
| 400 on assignee | Cloud needs accountId, not email/username |
| 404 project | Wrong `project_key` or no browse permission |
| 410 Gone | Endpoint removed by Atlassian — update `scripts/trackers/jira.py` |
