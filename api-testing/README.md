# API Testing Skill — Team Guide

A Claude skill that runs API testing the same way on every project: understand the API → design
test cases → automate → run → separate real bugs from noise → **show bugs to you and file them in
your project's bug tracker only after you approve**. Supported: ProofHub, Jira (Cloud and Data
Center), Trello, and a manual Markdown/CSV export for any other tool.

## What you change per project
Only **one file**: `api-test.config.yaml` in the project root (copy from
`assets/api-test.config.template.yaml`). Base URLs, login method, environments, and which bug tracker (`bug_tracker.type`) with its IDs.
Secrets are never written in it — only the names of environment variables.

## 5-minute setup
1. Install the skill in Claude (upload the `.skill` file, or put this folder in your skills dir).
2. Copy `assets/api-test.config.template.yaml` → `<project>/api-test.config.yaml`, fill it in.
3. Set secrets in your terminal, e.g.
   `export API_TOKEN=...` plus your tracker's credentials, e.g. `PROOFHUB_API_KEY`, or
   `JIRA_EMAIL` + `JIRA_API_TOKEN`, or `TRELLO_API_KEY` + `TRELLO_TOKEN` (Windows: `setx NAME "value"`).
4. `pip install pyyaml` (for helper scripts).
5. Find tracker IDs and check setup (see `references/trackers/<type>.md`):
   ```
   python scripts/bug_tracker.py lookup              # shows lookups for your tracker
   python scripts/bug_tracker.py lookup projects     # e.g. ProofHub/Jira projects, Trello: boards
   python scripts/bug_tracker.py doctor              # checks credentials and access
   ```

## Example prompts
| Level | Prompt |
|---|---|
| Fresher | "Here is our Swagger file. Write test cases for the Users API and explain each type." |
| Fresher | "Test this cURL and tell me if anything looks wrong." |
| Mid | "Generate a Pytest smoke suite for all P0 endpoints in docs/openapi.yaml and run it on qa." |
| Mid | "Here's the JUnit XML from last night's run. Triage the failures and draft bug reports." |
| Any | "Add integration tests for the login → cart → order flow." |
| Senior | "Add IDOR and mass-assignment checks to our existing Playwright API suite for /orders." |
| Senior | "Compare staging vs qa responses for /v2/invoices and report contract differences." |
| Any | "This project uses Jira (key PAY). Set up bug filing and log the approved bugs there." |

## What you get after a run (`api-test-reports/`)
- `test-cases.md` — what is tested, module-wise, split into positive and negative scenarios
- `test-report.md` / `.csv` — every scenario with expected, pass/fail, actual and linked bug
- `bugs/BUG-NNN.json` — bug drafts (with a plain-English description) and their tracker status

## How bug filing works (approval gate)
1. Claude triages failures (bug vs test problem vs environment).
2. For each real bug it shows a card: severity, endpoint, expected vs actual, steps, cURL,
   duplicate check result, and where it will be created.
3. You reply `create BUG-003`, `edit BUG-003: ...` or `skip BUG-003`.
4. Only then Claude runs `bug_tracker.py create ... --confirm`. Without `--confirm` the script
   never sends anything. It also blocks duplicates and masks tokens/passwords.

## Where it works
- **Claude Code** (terminal / VS Code / JetBrains): everything, including running tests and ProofHub.
- **Claude.ai chat**: design, code, triage, bug drafts. You run tests and the ProofHub command
  locally (the chat sandbox can't reach your servers).
- **CI**: run the suite; never auto-file bugs from CI.

## Folder map
```
SKILL.md                    workflow Claude follows
references/                 checklists and framework guides (Pytest, Playwright, REST Assured)
scripts/api_inventory.py    endpoint list from OpenAPI / Swagger / Postman
scripts/detect_stack.py     finds the project's existing test framework
scripts/parse_results.py    JUnit XML → summary + failures.json
scripts/test_report.py      test plan + results + bugs → module-wise test-report.md / .csv
scripts/bug_tracker.py      preview / create bugs in the configured tracker (approval enforced)
scripts/trackers/           one adapter per tool: proofhub, jira, trello, manual
assets/                     config template, test case / bug / summary templates
```

## Different tracker per project
Set `bug_tracker.type` in that project's config (`proofhub`, `jira`, `trello` or `manual`) and fill
that section. For a tool without an adapter (Azure DevOps, GitHub Issues, ClickUp...), use
`manual` today; adding an adapter is one Python file — see
`references/trackers/manual-and-new-trackers.md`.
