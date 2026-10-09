# BUG-AUTH-02: Login returns 201 instead of the documented 200

| Field | Value |
|---|---|
| **Bug ID** | BUG-AUTH-02 |
| **Module** | Auth |
| **Severity** | 🟢 Low |
| **Priority** | P4 |
| **Status** | Open |
| **Endpoint** | `POST /auth/login` |
| **Test case** | FS-AUTH-001 (positive, Happy path) |
| **Root cause** | BUG-011: POST /auth/login returns 201 instead of the documented 200 |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Login with valid credentials. Expected **200 + token (spec)**. Instead: spec documents 200 LoginResponse, got 201

## Why it matters
A successful login answers with a slightly different success code ('created') than the documentation says ('OK'). Login still works, but apps that check for the exact documented code may treat a good login as a failure.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/auth/login` and body `{"username":"mor_2314","password":"<PASSWORD>"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/auth/login' -H 'Content-Type: application/json' -d '{"username":"mor_2314","password":"<PASSWORD>"}'
```

## Expected result
200 + token (spec)

## Actual result
spec documents 200 LoginResponse, got 201

## Test reference
- Test: `tests/api/auth/test_login.py::test_FS_AUTH_001_login_with_valid_credentials`
- Failure message: `spec documents 200 LoginResponse, got 201`

[← Auth bugs](README.md) · [All bugs](../README.md)
