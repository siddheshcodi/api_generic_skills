# Bug reporting guide

A good API bug lets a developer reproduce the problem in under a minute without asking QA anything.

## Severity (impact) — pick the highest that applies
| Severity | Use when | API examples |
|---|---|---|
| Critical | Security breach, data loss/corruption, core flow fully blocked, no workaround | IDOR: user reads others' data; login always fails; payment charged twice; DELETE removes wrong record |
| High | Major feature broken or wrong, workaround is hard; any 5xx from client input | 500 on missing field; create returns 201 but nothing saved; wrong totals |
| Medium | Feature works partly; contract/validation problems that consumers will hit | Wrong status code (200 instead of 201/404); missing field in response; validation accepts invalid email |
| Low | Minor, cosmetic, no functional impact | Typo in error message; inconsistent field casing; 422 vs 400 when spec is loose |

## Priority (urgency) — business decides, QA suggests
P1 fix now / blocks release · P2 fix this sprint · P3 next sprints · P4 backlog.
Default suggestion: Critical→P1, High→P1/P2, Medium→P2/P3, Low→P3/P4.

## Title formula
`<METHOD> <path> <what goes wrong> when <condition>`
- Good: `POST /users returns 500 when email is missing`
- Good: `GET /orders/{id} returns another user's order (no ownership check)`
- Bad: `Users API not working`, `Bug in validation`, `Error 500`
The script adds `proofhub.title_prefix` (e.g. `[API]`) automatically — don't add it yourself.

## Required fields in the bug JSON (see assets/bug.example.json)
- `description` — **plain-English explanation for anyone** (freshers, PMs, clients, non-technical
  readers). It is shown first in the ticket and in the approval card. Rules:
  - 2–4 short sentences, no jargon: avoid status codes, JSON, field types, "endpoint", "schema".
    If a technical word is unavoidable, explain it ("the server says OK even though…").
  - Cover three things: **what happens now**, **what should happen instead**, **why it matters**
    (who is affected / what can go wrong).
  - Pattern: "When <user action>, the system <what it does now>. It should <correct behaviour>.
    This matters because <impact>."
  - Good: "Anyone on the internet can open the user list and see every customer's password in
    plain text. Passwords should never be shown to anyone. With these, a stranger can log in as
    any customer."
  - Bad: "GET /users response includes password field (CWE-200)." — that belongs in `actual`.
- `title`, `severity`, `priority`, `environment`, `method`, `endpoint`, `test_case_id`
- `steps` — numbered, start from a clean state, include auth role used
- `request.curl` — copy-paste runnable; secrets replaced with `<TOKEN>`, `<PASSWORD>`
- `expected` — what *should* happen, and the source (spec section, doc, confirmed by whom)
- `actual` — what happened: status, key part of body
- `response` — `status`, `time_ms`, `body` (trimmed), useful headers (request/correlation ID)
- `reproducibility` — e.g. `3/3`
- Optional: `test_case_ids` — every failed test with this root cause (links them in test-report.md),
  `affected_endpoints` (grouped bugs), `notes`, `attachments_note`

## Writing rules
- Facts, not blame. "Returns 500" not "developer forgot validation".
- One bug per root cause.
- Expected vs actual must be concrete and comparable.
- Never include real tokens, passwords, personal data from production. The script masks common
  secret patterns, but write them masked in the first place.
- Keep body excerpts short; mention if the full response is available in the test report.
