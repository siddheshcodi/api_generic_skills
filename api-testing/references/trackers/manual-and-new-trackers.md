# Manual export, and adding a new tracker

## Option 1 — `manual` (works today for any tool)
```yaml
bug_tracker: {type: manual, title_prefix: "[API]"}
manual:
  tool_name: "Azure DevOps"    # shown in previews so the user knows where to paste
  output_dir: ""               # default: <reports_dir>/bugs/export
```
After approval, `create --confirm` writes `BUG-NNN.md` (title + Markdown description, ready to
paste) and appends a row to `bugs.csv` (many tools can import CSV). Nothing is sent anywhere. The
same approval card, duplicate check (against earlier exports) and masking apply. Tell the user
the file path and ask them to paste/import it; when they share the tracker's ID, record it in the
bug JSON under `tracker.key`.

## Option 2 — add an adapter (one Python file, ~100 lines)
1. Copy `scripts/trackers/trello.py` (simplest) to `scripts/trackers/<name>.py`.
2. Implement the `Tracker` methods from `scripts/trackers/common.py`:
   | Method | Must do |
   |---|---|
   | `config_problems()` | Return missing required config keys (no network) |
   | `target()` | Text like "GitHub repo org/app (label bug)" for previews |
   | `build_payload(bug)` | Tool's create-request body. Use `self.title(bug)` and `self.description(bug)` (already masked) |
   | `preview_fields(payload)` / `preview_description(payload)` | What to show in the approval preview |
   | `find_duplicates(title)` | Search OPEN items; return `[{key, title, url, similarity}]` using `similarity()` and `DUPLICATE_THRESHOLD` |
   | `create(payload)` | Send it; return `{id, key, url}`; raise `TrackerError` on any failure |
   | `doctor()` | Lightweight auth + access check; return status lines |
   | `lookups()` | Optional helpers to find IDs for the config |
   Set `description_format` to `html`, `markdown`, `jira_wiki` or `text` — whatever the tool renders.
   Use `http_json()` for HTTP (handles errors, 429 retry) and `env_value()` for credentials.
3. Register it in `scripts/trackers/__init__.py` → `ADAPTERS`.
4. Add `references/trackers/<name>.md` (config, credentials, lookups, troubleshooting) and a row
   in the table in `references/bug-tracker-integration.md`.
5. Add the config section to `assets/api-test.config.template.yaml`.
6. Test with `doctor`, `preview --offline`, then one `create --confirm` on a sandbox project.
Never weaken the `--confirm` gate or masking in an adapter — they live in the shared code.

Quick API notes for common tools:
- **GitHub Issues:** `POST /repos/{owner}/{repo}/issues` `{title, body (markdown), labels, assignees}`;
  token in `Authorization: Bearer`; duplicates via `GET /search/issues?q=repo:o/r is:open in:title ...`.
- **Azure DevOps:** `POST {org}/{project}/_apis/wit/workitems/$Bug?api-version=7.1` with JSON-Patch
  body (`/fields/System.Title`, `/fields/Microsoft.VSTS.TCM.ReproSteps` as HTML); PAT via Basic auth.
- **GitLab:** `POST /projects/{id}/issues` `{title, description, labels}`; `PRIVATE-TOKEN` header.
Verify against the vendor's current docs before relying on these.
