# API Testing Framework (generic Claude skill)

A reusable API testing framework driven by a Claude skill: understand the API → design module-wise
positive and negative test cases → automate (Pytest / Playwright / REST Assured) → run → triage
failures → report → file bugs in your tracker (ProofHub, Jira, Trello or manual export) **only
after you approve each one**.

This repository is the **generic template**. It contains no project data. For each project you
clone it, and the clone becomes that project's main repo.

## Repository contents
| Item | What it is |
|---|---|
| `api-testing/` | The skill: workflow (`SKILL.md`), scripts, framework guides, templates |
| `api-testing.skill` | The same skill packaged — upload in Claude: Settings → Capabilities → Skills |
| `.gitignore` | Keeps secrets, virtual envs and caches out of every clone |

## Start a new project from this template
```bash
git clone <this-repo-url> my-project-api-tests
cd my-project-api-tests

# make the clone the project's own repo, keep the template for future skill updates
git remote rename origin template
git remote add origin <your-project-repo-url>
git push -u origin main
```
Then open the folder in Claude Code and say, for example:
> Use the api-testing skill on <API URL or spec file>. Set up the config, design module-wise
> positive and negative test cases, write the pytest suite, run it, triage the failures,
> generate the test report and show me the bug cards.

### What the project adds to the clone
```
my-project-api-tests/
├── api-testing/              ← generic skill (don't edit per project — see "Updating" below)
├── api-test.config.yaml      ← project: URLs, environments, auth env-var NAMES, bug tracker
├── docs/                     ← project: API spec (OpenAPI / Postman), if available
├── requirements-test.txt     ← project: test dependencies
├── pytest.ini                ← project: markers, test paths
├── tests/api/                ← project: one folder per module, one file per operation
│   ├── <module>/ ...
│   └── integration/
└── api-test-reports/         ← project: test-cases, test-report, bugs (commit if you want history)
```
The skill scripts find `api-test.config.yaml` in the project root automatically.

## Run and report (from the clone's root)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements-test.txt

pytest --junitxml=api-test-reports/junit.xml           # everything
pytest -m negative                                     # all negative tests
pytest -m "<module> and negative"                      # one module, one type
pytest -m integration                                  # cross-module flows

python api-testing/scripts/parse_results.py api-test-reports/junit.xml --out api-test-reports/results
python api-testing/scripts/test_report.py --cases api-test-reports/test-cases.json api-test-reports/junit.xml --out api-test-reports
python api-testing/scripts/bug_tracker.py doctor
python api-testing/scripts/bug_tracker.py preview api-test-reports/bugs/BUG-001.json
```
Helper scripts need Python 3.8+ and `pyyaml`.

## Secrets — never commit them
- `api-test.config.yaml` holds only the **names** of environment variables (e.g. `API_TOKEN`,
  `PROOFHUB_API_KEY`), never the values.
- Set values in your terminal or a local `.env` file (ignored by git). Never paste keys in chat.
- If a key is ever committed or shared, reset it in the tool that issued it.

## Bug trackers
Set `bug_tracker.type` to `proofhub`, `jira`, `trello` or `manual` and follow
`api-testing/references/trackers/<type>.md`. Start with `manual` — it writes Markdown + CSV to
`api-test-reports/bugs/export/` and sends nothing anywhere.

## Updating a project clone with skill improvements
Change the skill **here**, in the template repo, not inside a project clone. Then in each clone:
```bash
git pull template main      # brings in the new api-testing/ version
```
Project files never conflict because the template contains none of them.
After changing `api-testing/`, rebuild `api-testing.skill` (zip of the `api-testing/` folder).

## Known gaps (to fix later)
- Masking misses `curl -u user:pass` and `Cookie:` headers — check previews before approving.
- On production, write tests are skipped only if marked `destructive`.
- Two error messages mention `references/trackers/adding-a-tracker.md`; the real file is
  `manual-and-new-trackers.md`.
- Jira and Trello adapters are not yet verified against real accounts (ProofHub and manual are).
