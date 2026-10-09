# BUG-AUTH-01: Login with valid credentials

| Field | Value |
|---|---|
| **Bug ID** | BUG-AUTH-01 |
| **Module** | Auth |
| **Severity** | 🟢 Low |
| **Priority** | P4 |
| **Status** | Open |
| **Endpoint** | `POST /auth/login` |
| **Test case** | FS-AUTH-001 (positive) |
| **Category** | Response contract |
| **Root cause group** | BUG-005: POST /auth/login returns 201 instead of documented 200 on success |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Login with valid credentials. The API should return **200 + token (per spec)**. Instead: spec documents 200 LoginResponse, got 201.

## Why it matters
When a user logs in successfully, the system replies with a slightly different success code than the documentation says ("created" instead of plain "OK"). Login still works, so users won't notice, but apps that check for the exact documented code may wrongly treat a good login as a failure.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/auth/login` with: demo user (env FS_USER / FS_PASSWORD)
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/auth/login' -H 'Content-Type: application/json' -d '{"username":"<FS_USER>","password":"<FS_PASSWORD>"}'
```

## Expected result
200 + token (per spec)

## Actual result
spec documents 200 LoginResponse, got 201

201 Created with {"token":"<MASKED_JWT>"}

## Test reference
- Test: `tests/api/auth/test_login.py::test_FS_AUTH_001_login_with_valid_credentials`
- Failure message: `spec documents 200 LoginResponse, got 201`
