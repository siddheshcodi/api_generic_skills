# Test design checklist

Apply each section to every endpoint in scope. Not every item fits every endpoint — skip what
doesn't apply, but skip consciously. Each test case gets: ID, module, endpoint, title, type (`positive` / `negative`), category,
priority, tags, request, expected result (see `assets/test-cases.example.json`).
Section 2 = positive; sections 3, 4 (invalid side), 5, 9, 10 = mostly negative.

## Contents
1. Priorities and tags
2. Positive (happy path)
3. Input validation (negative)
4. Boundary values
5. Authentication and authorization
6. Response contract (status, schema, headers)
7. Resource lifecycle (CRUD chains)
8. List endpoints (pagination, filter, sort, search)
9. Error handling
10. Basic security checks
11. Basic performance and reliability
12. Coverage table per endpoint
13. Integration flows (cross-module)

## 1. Priorities and tags
| Priority | Meaning | Typical tag |
|---|---|---|
| P0 | Core flow; if broken the product is unusable (login, create order) | smoke |
| P1 | Important validation, auth, main error paths | smoke / regression |
| P2 | Boundaries, less common paths, filters | regression |
| P3 | Edge cases, cosmetic contract issues | regression |
Smoke set = all P0 + key P1; should run in a few minutes.

## 2. Positive (happy path)
- Valid request with only required fields → expected success code (200/201/204).
- Valid request with all optional fields → values stored and returned correctly.
- Response body values match the input (create then GET returns same data).
- Each enum value accepted at least once (for important enums).

## 3. Input validation (negative) — expect 400/422 with a clear message, never 500
- Each required field missing (one test per field for important endpoints).
- Wrong data type (string for number, number for string, object for array).
- Invalid format: email, uuid, date, phone, URL.
- Value not in enum.
- Empty string, whitespace-only, `null` for required fields.
- Unknown/extra fields (should be ignored or rejected — check what the spec says).
- Malformed JSON body; wrong `Content-Type`.
- Invalid path/query params (non-numeric ID, negative page number).

## 4. Boundary values (for every documented limit)
- Strings: minLength-1, minLength, maxLength, maxLength+1.
- Numbers: min-1, min, max, max+1; 0; negative; very large; decimals where integers expected.
- Arrays: empty, 1 item, max items, max+1.
- Dates: past, future, leap day, timezone edge if relevant.

## 5. Authentication and authorization
- No token → 401.
- Invalid / malformed token → 401.
- Expired token → 401 (if you can create one).
- Valid token, insufficient role → 403.
- **Object-level access (IDOR):** user A tries to read/update/delete user B's resource → 403/404,
  never 200. High-value test; include for every endpoint with an `{id}`.
- Sensitive data not returned to users who shouldn't see it (passwords, tokens, other users' PII).

## 6. Response contract
- Exact status code (not just "2xx").
- Body matches the schema: required fields present, correct types, no unexpected `null`.
- `Content-Type` header correct (usually `application/json`).
- Location header on 201 if the API uses it.
- Error responses follow the project's standard error format.

## 7. Resource lifecycle
- Create → Get → Update → Get (changed) → Delete → Get (404).
- Update non-existent ID → 404. Delete twice → 404 (or 204 if idempotent — check spec).
- Duplicate create (same unique field) → 409 or 400, not 500.
- Partial update (PATCH) changes only the sent fields.

## 8. List endpoints
- Default page size; first page, last page, page beyond last (empty list, not error).
- page size 0, negative, above max.
- Filters: each filter alone, combined, no match (empty list).
- Sort: asc/desc, invalid sort field → 400.
- Search with special characters and empty string.
- Total count consistent with returned items.

## 9. Error handling
- No 500 for any client mistake. Any 5xx from bad input is a bug.
- Error messages are helpful but don't leak stack traces, SQL, file paths, internal hostnames.
- Unsupported HTTP method → 405.
- Non-existent route → 404.

## 10. Basic security checks (safe, non-destructive)
Only on non-production unless the user allows. These are smoke checks, not a pentest.
- SQL-like input (`' OR '1'='1`) in string fields/query → handled as plain text, no 500, no data leak.
- Script input (`<script>alert(1)</script>`) stored and returned escaped or rejected.
- Very long string (10k chars) → 400/413, not 500 or hang.
- Mass assignment: send fields the user shouldn't control (`role`, `isAdmin`, `balance`) → ignored.
- HTTPS enforced; sensitive data not in URLs/query strings.

## 11. Basic performance and reliability
- Response time under `defaults.max_response_time_ms` for P0 calls (report slow ones as
  observations; file as bug only if clearly beyond agreed SLA).
- Same GET called twice returns same result (consistency).
- Idempotent methods (PUT, DELETE) safe to repeat.
- Real load testing is out of scope — suggest k6/JMeter if the user needs it.

## 12. Coverage table (include in test-cases.md)
| Endpoint | Positive | Validation | Boundary | Auth | Contract | Lifecycle | List | Security | Total |
|---|---|---|---|---|---|---|---|---|---|
Fill with counts; use "–" for not applicable. Makes gaps obvious to reviewers.

## 13. Integration flows (cross-module) — `integration/` folder, module `Integration`
Tests that need two or more modules to work together. Pick the flows real users do:
- **Business flow:** login → create order → pay → order status changes; user signs up → can log in.
- **Data consistency:** every ID one resource points to exists in the other (cart → product,
  order → user); list and detail endpoints return the same data; totals match line items.
- **Side effects:** deleting a user removes/blocks their orders; changing a price affects new
  carts only.
- **Auth across modules:** a token from login works on every protected module; after logout it
  works on none.
Keep each flow independent (create its own data, clean up). If the API does not persist writes
(mock/sandbox APIs), use read-only consistency flows and note the gap in assumptions.
