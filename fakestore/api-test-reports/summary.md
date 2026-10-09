# API test summary — Fake Store API — 2026-10-09

**Environment:** public (https://fakestoreapi.com) · **Framework:** pytest · **Source:** `docs/openapi.json` (OpenAPI 3.1, 16 endpoints) + website docs · **Scope:** Products, Carts, Users, Auth (24 operations incl. limit/sort/date/category/PATCH) + Integration flows · **Run type:** full regression, failures re-run 3×

Full module-wise detail: `test-report.md` / `test-report.csv`. Readable bug files per module: `../bug-reports/README.md`.

## Result
| Test cases | Test runs | Passed | Failed | Errors | Skipped | Pass rate (runs) | Positive cases pass | Negative cases pass |
|---|---|---|---|---|---|---|---|---|
| 101 | 115 | 67 | 48 | 0 | 0 | 58.3% | 38/42 (90.5%) | 23/59 (39.0%) |

Normal reads, list options (limit, sort, date range, category) and all 10 cross-module flows work. The API fails most negative checks: it rarely rejects bad input or unknown ids, requires no login for any change, and exposes passwords. Every failure reproduced 3/3.

## Bugs (12 root causes → 48 individual bugs; tracker: manual, nothing filed)
| Root cause | Severity | Title | Bugs |
|---|---|---|---|
| BUG-001 | Critical | GET /users, /users/{id}, DELETE /users/{id} return passwords in plain text (and they work for login) | 3 |
| BUG-002 | High | Products, carts and users can be created, changed and deleted without logging in | 3 |
| BUG-003 | High | Login tokens never expire (no `exp` claim) | 1 |
| BUG-004 | Medium | POST /users gives new users an existing user's id (1) in ~40% of calls | 1 |
| BUG-005 | Medium | Unknown/invalid ids return 200 with empty, null or made-up records | 13 |
| BUG-006 | Medium | Create/update accept empty and invalid data (products, carts, users) | 18 |
| BUG-007 | Medium | Duplicate username accepted | 1 |
| BUG-008 | Medium | Cart items do not match the documented Cart schema | 1 |
| BUG-009 | Medium | POST/PUT/PATCH /users do not return the user record | 3 |
| BUG-010 | Low | Errors returned as plain text / HTML instead of JSON | 2 |
| BUG-011 | Low | Login returns 201 instead of documented 200 | 1 |
| BUG-012 | Low | X-Powered-By: Express header on every response | 1 |

## Not bugs (handled)
- Test fixes made: none needed after the first run; every failure matched the live probing done before writing tests.
- Environment issues: none (no timeouts, 5xx or rate limits; responses 0.4–1.6 s).
- The client sends requests without a cookie jar and retries on 429, same as the skill's other projects.

## Needs clarification
- The spec defines no authentication or required fields. BUG-002 (writes without login) and parts of BUG-006 rely on security / common-sense expectations; confirm with the API owner.
- `?limit=-1`, `?limit=abc`, `?sort=sideways` are silently ignored (full list returned). Parameters are not in the spec, so this is recorded as passing (no 5xx).

## Observations (not filed)
- Category name `jewelery` is misspelled in the data.
- `/carts/user/9999` returns `[]` (accepted as "no carts"), while `/carts/9999` returns `null`.
- New carts get id 11 although only 7 carts exist.
- Plain HTTP correctly redirects (301) to HTTPS; CORS is open (`Access-Control-Allow-Origin: *`).

## Coverage gaps / next steps
- Writes are not persisted, so create → read → update → delete lifecycles cannot be verified.
- Token usage on protected routes cannot be tested: no endpoint requires a token.
- Load / rate-limit behaviour not tested (out of scope).
- To file in ProofHub: set `bug_tracker.type: proofhub` and the `proofhub:` block in `api-test.config.yaml`, then preview and approve each bug.
