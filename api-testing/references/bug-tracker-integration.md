# Bug tracker integration (common rules for every tracker)

The tracker is chosen per project in `api-test.config.yaml`:
```yaml
bug_tracker:
  type: proofhub        # proofhub | jira | trello | manual
  title_prefix: "[API]"
```
Each tracker has its own section (`proofhub:`, `jira:`, `trello:`, `manual:`). Only the section
for the chosen type needs to be filled. Read the matching file in `references/trackers/`:

| type | File | Bugs become |
|---|---|---|
| `proofhub` | `trackers/proofhub.md` | Tasks in a task list |
| `jira` | `trackers/jira.md` | Issues (type Bug) in a project — Cloud or Data Center |
| `trello` | `trackers/trello.md` | Cards in a list |
| `manual` | `trackers/manual-and-new-trackers.md` | Markdown + CSV export to paste into any other tool |

If the project's tool isn't listed (Azure DevOps, GitHub Issues, ClickUp, Linear, Redmine, Asana,
...), use `manual` today and see `trackers/manual-and-new-trackers.md` to add an adapter later.

## One CLI for all trackers
```
python <skill>/scripts/bug_tracker.py doctor                 # config + credentials + access
python <skill>/scripts/bug_tracker.py lookup                 # what lookups this tracker has
python <skill>/scripts/bug_tracker.py lookup <name> [...]    # find IDs for the config
python <skill>/scripts/bug_tracker.py preview BUG-001.json   # exact payload + duplicate check
python <skill>/scripts/bug_tracker.py create BUG-001.json --confirm   # ONLY after approval
```
`--tracker <type>` overrides the config for one run. Run from the project root (or `--config`).

## Rules that are the same for every tracker (enforced by the script)
- `create` without `--confirm` → preview only, exit code 2, nothing sent.
- One bug per `create` call, so each bug is approved individually.
- Duplicate check against open items before creating → exit code 3 if similar items exist,
  unless `--allow-duplicate` (pass it only after the user chose "create anyway").
- Bug files with status `created` are never created again; status `skipped` is refused.
- Secrets (Bearer/Basic tokens, JWTs, `password`, `api_key`, `token`, `secret`) are masked in
  every title, description and error message.
- After creating, the bug JSON gets `"status": "created"` and
  `"tracker": {"type", "id", "key", "url"}` — used in the summary report.
- Credentials only from environment variables named in the config.

## Using a connected Claude connector instead of the script
If the session has a connector for the project's tracker (for example an Atlassian/Jira connector
in the Claude app), Claude may use it — useful in the chat app where the script can't reach the
tracker. The same rules still apply:
1. Run `bug_tracker.py preview <bug> --offline` (or render the same fields) to get the masked
   title, description and field values.
2. Search for duplicates with the connector's search tool (e.g. JQL like the Jira adapter's).
3. Show the approval card; wait for explicit approval of that bug.
4. Create with the connector using exactly the previewed values.
5. Update the bug JSON: `"status": "created"` and `"tracker": {...}` with the returned key/URL.
Never use a connector to create anything the user hasn't approved in chat.

## Severity mapping across trackers
Severity (Critical/High/Medium/Low) is always in the title as `[High]` and in the description.
Each tracker also maps it to its own field: ProofHub label IDs, Jira priority names (+ a
`severity-high` label), Trello label IDs, manual CSV column.
