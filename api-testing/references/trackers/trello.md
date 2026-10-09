# Tracker: Trello

Set `bug_tracker.type: trello`. Common rules: `../bug-tracker-integration.md`.
Uses Trello REST API v1. Bugs become cards (Markdown description) in a list such as "Bugs".

## Config
```yaml
trello:
  api_key_env: "TRELLO_API_KEY"
  token_env: "TRELLO_TOKEN"
  board_id: ""             # used for lookups and board-wide duplicate check
  list_id: ""              # list where new bug cards go
  severity_labels: {Critical: "", High: "", Medium: "", Low: ""}   # label IDs
  extra_labels: []         # e.g. an "API" label ID
  default_members: []      # member IDs
  position: top            # top | bottom
```

## Credentials
1. Create a Power-Up / API key at https://trello.com/power-ups/admin (gives the API key).
2. From that page, generate a **token** for your account.
3. Set `TRELLO_API_KEY` and `TRELLO_TOKEN` in your terminal.
The script sends them in the `Authorization: OAuth ...` header, never in the URL.

## Find values
```
python <skill>/scripts/bug_tracker.py lookup boards                 # → board_id
python <skill>/scripts/bug_tracker.py lookup lists --board <id>     # → list_id
python <skill>/scripts/bug_tracker.py lookup labels --board <id>    # → severity_labels
python <skill>/scripts/bug_tracker.py lookup members --board <id>   # → default_members
python <skill>/scripts/bug_tracker.py doctor
```
Tip: create labels Critical/High/Medium/Low on the board first (colors red/orange/yellow/green).

## Duplicate check
Open cards on the whole board (if `board_id` set) or in the list, compared by title similarity.
Cards moved to other lists (e.g. "In progress") are still found when `board_id` is set.

## Troubleshooting
| Error | Fix |
|---|---|
| 401 "invalid key/token" | Regenerate the token; check both env vars |
| 404 on list | Wrong `list_id`, or the token's account isn't on the board |
| Labels missing on card | Label IDs belong to another board — re-run `lookup labels` |
