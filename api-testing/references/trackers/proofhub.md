# Tracker: ProofHub

Set `bug_tracker.type: proofhub` in the config. Common rules (approval gate, CLI) are in
`../bug-tracker-integration.md`.

Uses ProofHub REST API v3 (official docs: https://github.com/ProofHub/api_v3).
Bugs are created as **tasks** inside a task list (e.g. a "Bugs" or "API Bugs" list) of a project.

## One-time setup per person
1. Get your API key: in ProofHub click your profile icon → **API access** → copy the key.
   (Resetting the key disconnects old integrations.)
2. Store it as an environment variable — never in the config file, never in chat:
   - macOS/Linux: `export PROOFHUB_API_KEY="..."` (add to `~/.zshrc` / `~/.bashrc`)
   - Windows PowerShell: `setx PROOFHUB_API_KEY "..."` then open a new terminal
3. `pip install pyyaml` (only dependency of the helper scripts).

## One-time setup per project (fill `proofhub:` in api-test.config.yaml)
Run these from the project root (they only read data):
```
python <skill>/scripts/bug_tracker.py lookup projects                    # → project_id
python <skill>/scripts/bug_tracker.py lookup todolists --project <id>    # → todolist_id of "Bugs" list
python <skill>/scripts/bug_tracker.py lookup labels                      # → severity_labels IDs
python <skill>/scripts/bug_tracker.py lookup people                      # → default_assignees IDs
python <skill>/scripts/bug_tracker.py doctor                             # checks everything
```
`company` is the subdomain in `https://<company>.proofhub.com`.
Tip: create labels named Critical / High / Medium / Low in ProofHub if they don't exist.

## What the script sends
`POST https://<company>.proofhub.com/api/v3/projects/<project_id>/todolists/<todolist_id>/tasks`
Headers: `X-API-KEY`, `User-Agent: <config user_agent>` (required by ProofHub, else 400),
`Content-Type: application/json`.
Body: `title`, `description` (formatted HTML built from the bug JSON), `assigned` (people IDs),
`labels` (severity label + extra labels), optional `custom_fields`.

## Custom fields (optional)
ProofHub custom fields are keyed by field ID. Map a bug value into one:
```yaml
custom_fields:
  "6768923873":            # e.g. a "Severity" dropdown field
    from: severity         # any key of the bug JSON
    values:                # optional: map bug value -> ProofHub value (dropdown/tag use option IDs in a list)
      Critical: ["740974745"]
      High: ["740974746"]
  "6798922309":
    from: environment      # plain text field, value passed as-is
```
If a value doesn't match the field type, ProofHub replies 200 with an error code (2033); the script
detects this and reports it instead of claiming success.

## ProofHub specifics
- Duplicate check looks at open (not completed) tasks in the configured task list.
- Rate limit is 25 requests / 10 s; on HTTP 429 the script waits `Retry-After` and retries once.

## Troubleshooting
| Error | Fix |
|---|---|
| `PROOFHUB_API_KEY not set` | Export the variable in the same terminal Claude uses; restart the session |
| 400 Bad Request | `user_agent` missing/empty in config |
| 401 / 403 | Wrong key, or your user has no access to that project/list |
| 404 | Wrong `company`, `project_id` or `todolist_id` — re-run the lookup commands |
| 415 | Content-Type issue — use the script, don't hand-craft calls |
| code 2033 | Custom field value doesn't match field type — fix `custom_fields` mapping |
| Proxy / connection blocked | You're in a sandbox (e.g. chat app). Run the command on your own machine |

## Optional: clickable link
ProofHub task URLs differ by account setup. Open any task in your browser, copy its URL, replace
the task number with `{task_id}` (or `{ticket}`, `{project_id}`, `{todolist_id}`), and save it as
`task_url_template`. The script then prints a direct link after creating.
