# Running environments

## Claude Code (terminal, VS Code, JetBrains, desktop Code tab) — full workflow
- Claude can read the repo, write tests, run them, parse results and call ProofHub.
- Secrets come from the shell environment or a local `.env` that is git-ignored. Check with
  `python scripts/bug_tracker.py doctor` before the first bug is filed.
- Python 3.8+ is needed for the helper scripts (`pip install pyyaml` once). The tests themselves
  use the project's own language.

## Claude.ai chat app — design + analysis mode
The chat sandbox can reach only a small allow-list of hosts (package registries, GitHub). Company
APIs and bug trackers (ProofHub, Jira, Trello...) are normally blocked by the sandbox. So:
1. User uploads/pastes the spec, collection, cURL or docs (and optionally the config file).
2. Claude produces inventory, test cases and test code as downloadable files.
3. User runs the tests locally and uploads the JUnit XML (or pastes the failure output).
4. Claude runs `parse_results.py` on the upload, triages, and writes bug JSON drafts.
5. Approval card shown in chat. For approved bugs, either:
   - use a connected tracker connector if the session has one (e.g. Jira via an Atlassian
     connector) following `bug-tracker-integration.md`, or
   - give the user the bug file(s) and the command
     `python scripts/bug_tracker.py create bugs/BUG-003.json --confirm`
     to run on their machine, where the skill folder and credentials exist.
If a network call fails with a proxy / "x-deny-reason" error, say the host is blocked in this
environment and switch to this mode. An org owner can change allowed domains if needed.

## CI (GitHub Actions, GitLab, Jenkins)
- Run the generated suite with JUnit output as a normal pipeline step.
- **Never** create tracker issues automatically from CI — that would skip the approval gate.
  Publish `failures.json` and the JUnit report as artifacts; a person then opens Claude, triages,
  and approves bugs.
