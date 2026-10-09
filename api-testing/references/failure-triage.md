# Failure triage — is it really a bug?

Filing a false bug costs developer time and trust in QA. Check each failure in this order.

## Step A — Environment problem? (check first, it explains many failures at once)
Signs: many unrelated tests fail together; connection refused / DNS / timeout; 502/503/504 from a
gateway; 401 on *every* test (expired or missing token); SSL errors.
→ Verify with one simple call (health endpoint or a basic GET). Report to the user as an
environment issue. Do **not** file bugs. Rerun when fixed.

## Step B — Test problem?
Signs: assertion expects something the spec never promised; test data collides with existing data
(duplicate key from a previous run); hard-coded ID that doesn't exist here; order-dependent tests;
typo in path; schema in the test is outdated vs spec.
→ Fix the test, rerun, and list the fix in the summary ("test fixes made").

## Step C — Is the expected behaviour actually defined?
- Spec/docs clearly define it → continue to Step D.
- Spec silent or contradictory → **Needs clarification**. Ask the user. If they confirm the
  expectation, treat it as a bug; record who confirmed it in the bug's `notes`.
- Exception: a 5xx caused by client input, a security issue (IDOR, data leak, stack trace) or data
  corruption is a bug even if the spec says nothing.

## Step D — Reproduce
- Rerun the single test (or the cURL) at least once more; for flaky-looking cases, 3 times.
- Record reproducibility, e.g. `3/3` or `2/5 (intermittent)`. Intermittent bugs are still valid —
  mark them so.
- Capture: exact request (with secrets masked), status, response body (trim to the useful part,
  ~2,000 chars max), response time, timestamp, environment, any request/correlation ID header.

## Step E — Group duplicates before drafting
- Same root cause across endpoints (e.g. every endpoint returns 500 on malformed JSON) → one bug
  listing all affected endpoints, not ten bugs.
- Same symptom, clearly different code paths → separate bugs.

## Quick decision table
| Observation | Verdict |
|---|---|
| 500 on invalid input | API bug (usually High) |
| 200 when accessing another user's resource | API bug (Critical) |
| 400 expected, got 422 (spec says 400) | API bug (Low) — or Needs clarification if spec is vague |
| Schema mismatch: field missing / wrong type | API bug (Medium/High depending on consumer impact) |
| Everything 401 | Environment (token) |
| Everything times out | Environment |
| Duplicate key error on create, only on rerun | Test problem (data not unique/cleaned) |
| Slow response once, fast on rerun | Observation, not a bug |
