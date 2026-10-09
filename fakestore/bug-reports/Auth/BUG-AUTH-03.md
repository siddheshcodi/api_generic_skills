# BUG-AUTH-03: Login errors are plain text, not JSON

| Field | Value |
|---|---|
| **Bug ID** | BUG-AUTH-03 |
| **Module** | Auth |
| **Severity** | 🟢 Low |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /auth/login` |
| **Test case** | FS-AUTH-010 (negative, Contract) |
| **Root cause** | BUG-010: Error responses are plain text or HTML pages instead of JSON |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Login errors are returned as json. Expected **error body is JSON**. Instead: error body is 'text/html; charset=utf-8', not JSON: 'username or password is incorrect'

## Why it matters
When something goes wrong at login (wrong password, missing fields) or the request is badly formed, the system answers with plain text or a web page instead of the structured format it uses everywhere else. Apps can't read these errors reliably and may crash or show raw HTML to the user.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/auth/login` and body `{"username":"mor_2314","password":"wrong-password"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/auth/login' -H 'Content-Type: application/json' -d '{"username":"mor_2314","password":"wrong-password"}'
```

## Expected result
error body is JSON

## Actual result
error body is 'text/html; charset=utf-8', not JSON: 'username or password is incorrect'

## Test reference
- Test: `tests/api/auth/test_login.py::test_FS_AUTH_010_login_errors_are_returned_as_json`
- Failure message: `error body is 'text/html; charset=utf-8', not JSON: 'username or password is incorrect'`

[← Auth bugs](README.md) · [All bugs](../README.md)
