---
name: api-testing
description: Complete API testing workflow for any REST/HTTP API project. Reads OpenAPI/Swagger specs, Postman collections, cURL commands or plain API docs; designs test cases (positive, negative, boundary, auth, schema, security basics); writes and runs automated tests in Pytest, Playwright or REST Assured (auto-detected per project); triages failures into real bugs vs test or environment problems; and files bugs in the project's bug tracker (ProofHub, Jira, Trello, or a manual export for any other tool) only after the user explicitly approves each one. Use this skill whenever the user mentions API testing, endpoint testing, API QA, Swagger/OpenAPI, Postman collections, API test cases or test plans, API automation, contract or schema validation, API smoke/regression tests, API bug reports, or logging bugs in ProofHub, Jira, Trello or any bug tracker — even if they only say "test this endpoint", "check this API" or paste a cURL command.
---

# API Testing Skill

This skill turns Claude into a disciplined API QA engineer. The **process** is the same on every
project; everything project-specific (URLs, auth, environments, which bug tracker and its IDs) lives in one file:
`api-test.config.yaml` in the project root. Adapting to a new project = filling in that file.

## Golden rules (never break these)

1. **No bug is filed in any tracker without explicit approval.** Show every bug in full first, then ask. Only an
   explicit "yes / create / approve" from the user in chat for *that* bug counts. Approval does not
   carry over to new bugs found later. The script enforces this too: it refuses to create without
   `--confirm`, and Claude adds `--confirm` only after the user's yes.
2. **No secrets in files or chat.** Config holds the *names* of environment variables, never values.
   Never print tokens or passwords; mask them in bug reports (the bug tracker script also masks them).
3. **Protect production.** If the target environment has `is_production: true`, run only read-only
   tests (GET/HEAD/OPTIONS) unless config sets `allow_destructive_on_production: true`. Say so.
4. **Only real bugs become bug reports.** Every failure is triaged first (Step 7). Test-script
   mistakes and environment outages are fixed or reported to the user, not filed as bugs.
5. **Match the user's level.** If the user seems new to QA, explain terms briefly in plain words
   (e.g. "schema = the expected shape of the response"). Experienced users get concise output.

## Where am I running?

Check which tools are available before promising anything.

| Capability | Claude Code / terminal / CI | Claude.ai chat app |
|---|---|---|
| Read spec / Postman / docs | Yes | Yes (uploaded or pasted) |
| Design test cases, write test code | Yes | Yes |
| Run tests against the API | Yes | Usually **no** — sandbox blocks most outside hosts |
| File bug in tracker | Yes (after approval) | Only via a connected tracker connector (e.g. Jira); otherwise prepare bug JSON + exact command for the user |

In the chat app: design the tests, generate the code as files, ask the user to run them locally
and upload the JUnit XML result (or paste failures), then triage and prepare bug drafts. For
approved bugs, give the user the bug JSON file and the one-line command to run on their machine.
Read `references/environments.md` for details.

## Workflow

Script paths below are relative to this skill's folder. Run them with the project root as the
current directory so they find `api-test.config.yaml` (or pass `--config`).

Follow the steps in order. Small requests ("test this one endpoint") can compress steps 1–4 into a
few lines, but never skip triage (7) or the approval gate (8).

### Step 1 — Load project config
- Look for `api-test.config.yaml` in the project root (or ask the user where it is).
- If missing: copy `assets/api-test.config.template.yaml` to the project root and fill it in with
  the user. Ask only for what you need now (base URL + auth for testing; bug tracker type and IDs only
  when a bug is about to be filed). Explain that this file is the only per-project change.
- Confirm the target environment (default: `environments.default`). Note if it is production.

### Step 2 — Understand the API
- Read `references/input-sources.md` for how to handle each input type.
- For OpenAPI/Swagger or Postman, run:
  `python scripts/api_inventory.py <spec-or-collection> --out <reports_dir>/inventory`
  This produces an endpoint inventory (method, path, params, body, responses, auth).
- For cURL/docs, build the same inventory by hand using `assets/test-case-template.md` columns.
- List assumptions and unclear behaviour (e.g. "spec doesn't say what happens on duplicate email").
  These become questions for the user or "Needs clarification" items — never invented expectations.

### Step 3 — Pick the framework
- `framework` in config wins. If `auto`, run `python scripts/detect_stack.py <project-dir>`.
- Existing test suite found → follow its style, folders and helpers. Don't create a parallel one.
- Nothing found → recommend **Pytest** for new suites (simplest for freshers) unless the team's
  stack is clearly JS/TS (→ Playwright) or Java (→ REST Assured). Confirm with the user once.
- Read exactly one framework reference: `references/framework-pytest.md`,
  `references/framework-playwright.md` or `references/framework-restassured.md`.

### Step 4 — Design test cases
- Read `references/test-design-checklist.md` and apply it to every endpoint in scope.
- Group cases **by module** (one module = one resource / tag, e.g. Products, Carts, Auth) and mark
  every case `positive` (valid input, expect success) or `negative` (invalid input, missing/wrong
  auth, unknown IDs, bad data — expect a clean error). Aim for both types in every module.
- Save the plan as `<reports_dir>/test-cases.json` following `assets/test-cases.example.json`
  (ID format `<module_prefix>-<MODULE>-<NNN>`, priority P0–P3, tags `smoke` / `regression`).
  This file is the single source of truth for "what is tested"; the report is built from it.
- Render the readable plan: `python scripts/test_report.py --cases <reports_dir>/test-cases.json
  --plan-only --out <reports_dir>` → `test-cases.md` (module-wise, positive and negative tables).
- For big APIs, start with P0/P1 smoke coverage, show the plan summary (counts per module,
  positive/negative) and let the user widen scope.

### Step 5 — Write the automated tests
- Follow the framework reference: shared config loader, one auth helper, schema checks on every
  2xx response, test-case ID from `test-cases.json` in every test name (that is how results are
  matched to the plan).
- **Structure** (same idea in all three frameworks):
  - One **folder per module** (`products/`, `users/`...), one **file per operation** inside it
    (`test_list_products`, `test_get_product`, `test_create_product`...). Positive and negative
    tests of the same operation live in the same file — never split files by test type.
  - Every test carries a **type marker/tag** `positive` or `negative` (plus `smoke`/`regression`);
    the module marker comes from the folder. Run any slice with markers (e.g. negative tests of
    one module) instead of moving files.
  - Cross-module flows go in one top-level **`integration/`** folder (module `Integration` in
    `test-cases.json`), not inside a module.
  - Very small APIs (≤ ~20 tests per module) may use one file per module; switch to folders as
    soon as a module grows.
- Test data: prefix with `testing.test_data_prefix`, generate unique values, clean up after
  (`cleanup_test_data`). Never hard-code IDs that only exist on one machine.

### Step 6 — Run the tests
- Always produce JUnit XML (all three frameworks support it — commands are in each reference).
- Then run: `python scripts/parse_results.py <junit.xml...> --out <reports_dir>/results`
  This gives a pass/fail summary and a `failures.json` list to triage.
- Chat app: give the user the run command, ask them to upload the XML.

### Step 7 — Triage every failure
Read `references/failure-triage.md`. For each failure decide one of:
- **API bug** → goes to Step 8.
- **Test issue** (wrong expectation, bad data, script error) → fix the test, rerun, tell the user.
- **Environment issue** (timeouts everywhere, 502/503, expired token, DNS) → report to user, don't file.
- **Needs clarification** (spec silent or contradictory) → ask the user / product owner.
Re-run each suspected bug once to confirm it reproduces before drafting a report.

### Step 8 — Bug drafts → approval → bug tracker
1. Read `references/bug-reporting.md` (severity rules + writing guide).
2. For each confirmed bug, write `<reports_dir>/bugs/BUG-<NNN>.json` following
   `assets/bug.example.json`. Include a ready-to-run cURL with secrets replaced by `<TOKEN>`.
   Always write `description`: a plain-English explanation a non-technical reader understands
   (what happens now, what should happen instead, why it matters — rules in bug-reporting.md).
   The script refuses bug files without it.
3. Run `python scripts/bug_tracker.py preview <bug files>` — this shows exactly what will be sent
   to the configured tracker (`bug_tracker.type`) and checks it for possible duplicates.
4. Present each bug in chat using the **Approval card** format below, then stop and wait.
5. Act on the answer per bug:
   - **Create** → `python scripts/bug_tracker.py create <file> --confirm`, then share the
     ticket key / link the script prints.
   - **Edit** → apply changes to the JSON, show the card again, ask again.
   - **Skip** → mark `"status": "skipped"` in the JSON, don't file.
   - Unclear answer → ask again. Silence is not approval.
6. If a possible duplicate is reported, show it and ask: comment on existing / create anyway / skip.
   Only pass `--allow-duplicate` after the user chooses "create anyway".

Read `references/bug-tracker-integration.md` before the first bug in a session, then the file for
the project's tracker in `references/trackers/` (proofhub, jira, trello, manual-and-new-trackers)
for setup, `lookup` commands and troubleshooting. If the tool has no adapter, use `manual`.
If a connector for the tracker is connected in this session, it may be used instead of the script
— same preview, duplicate check and approval rules (see bug-tracker-integration.md).

### Step 9 — Test report
1. Run `python scripts/test_report.py --cases <reports_dir>/test-cases.json <junit.xml...>
   --out <reports_dir>`. It joins plan + results + `bugs/*.json` into:
   - `test-report.md` — overall result, positive vs negative pass rate, module summary, then per
     module every scenario with expected, result (pass/fail), actual on failure and linked bug;
   - `test-report.csv` — same rows for Excel / Google Sheets / test-management import.
   Rerun it after bugs are created so tracker keys appear. Check its "Notes for triage" section:
   every failure must be linked to a bug (`test_case_id` / `test_case_ids` in the bug JSON) or
   explained as a test/environment issue.
2. Write `<reports_dir>/summary.md` using `assets/test-summary-template.md` for the narrative
   (test fixes made, environment issues, open questions, coverage gaps).
3. Give the user a short version in chat: overall + per-module counts and the bug list.

## Approval card (use this exact layout in chat)

```
🐞 BUG-003 — [High] POST /users returns 500 when "email" is missing
In simple words: When someone creates a user without an email, the server crashes instead of
  saying "email is required". It should show a clear message so they can fix it and retry.
Endpoint: POST {base_url}/users        Env: qa        Test: API-USERS-004
Expected: 400 Bad Request with a validation message for "email"
Actual:   500 Internal Server Error, body: {"error":"NullPointerException"}
Repro:    3/3 runs          Possible duplicate: none found
Steps:
  1. Send POST /users with a valid token and body {"name":"qa_auto_x"} (no email)
  2. Observe the status code and body
cURL:  curl -X POST "{base_url}/users" -H "Authorization: Bearer <TOKEN>" -d '{"name":"qa_auto_x"}'
Will be created in: <tracker target from preview>, priority/labels: High, assignee: <...>

➡️ Create this in <Jira/ProofHub/Trello>? Reply: "create BUG-003", "edit BUG-003: ...", or "skip BUG-003".
```

When several bugs are found, show all cards, then one question. The user may approve some and
skip others ("create 1 and 3, skip 2"). "Create all" is valid only for the cards shown right then.

## Output files (inside `testing.reports_dir`, default `api-test-reports/`)

```
api-test-reports/
├── inventory/            endpoints.md + endpoints.json   (Step 2)
├── test-cases.json       designed test cases, module-wise, positive/negative (Step 4)
├── test-cases.md         readable plan generated from test-cases.json      (Step 4)
├── junit.xml             raw run result                                    (Step 6)
├── results/              summary.md + failures.json                        (Step 6)
├── bugs/BUG-NNN.json     one file per bug, status draft/created/skipped    (Step 8)
├── test-report.md        module-wise pass/fail report with linked bugs     (Step 9)
├── test-report.csv       same, for Excel / test-management tools           (Step 9)
└── summary.md            narrative summary                                 (Step 9)
```
Test code goes in the project's normal test folder (see framework reference), not in reports.

## When a project needs more than config
Keep changes small and local to the project, never inside this skill:
- Unusual auth (signed requests, multi-step SSO): add one auth helper in the project's test folder.
- Extra tracker fields: map them under `<tracker>.custom_fields` in config.
- Different bug tracker: change `bug_tracker.type` and fill that section. A tool with no adapter
  uses `manual` now; adding an adapter is one Python file
  (`references/trackers/manual-and-new-trackers.md`). The workflow never changes.

## Reference map
| File | Read when |
|---|---|
| `references/input-sources.md` | Step 2 — handling OpenAPI, Postman, cURL, docs |
| `references/test-design-checklist.md` | Step 4 — what to test for each endpoint |
| `assets/test-cases.example.json` | Step 4 — format of the test plan (module, positive/negative) |
| `references/framework-pytest.md` / `-playwright.md` / `-restassured.md` | Steps 5–6 — only the chosen one |
| `references/failure-triage.md` | Step 7 |
| `references/bug-reporting.md` | Step 8 — severity and writing rules |
| `references/bug-tracker-integration.md` | Step 8 — rules shared by all trackers, connectors |
| `references/trackers/<type>.md` | Setup, lookups, errors for proofhub / jira / trello / manual |
| `references/environments.md` | Running in chat app vs Claude Code vs CI |
