# BUG-AUTH-01: Login token never expires (no 'exp' claim)

| Field | Value |
|---|---|
| **Bug ID** | BUG-AUTH-01 |
| **Module** | Auth |
| **Severity** | 🟠 High |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /auth/login` |
| **Test case** | FS-AUTH-003 (negative, Security) |
| **Root cause** | BUG-003: POST /auth/login issues tokens that never expire |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Token has an expiry. Expected **token has an 'exp' (expiry) claim**. Instead: token has no 'exp' claim and never expires: claims ['iat', 'sub', 'user']

## Why it matters
The login key the system hands out after signing in never runs out. If someone steals it (from a shared computer, a log file or a browser), they can use it forever. Login keys should expire after a set time, for example one hour.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/auth/login` and body `{"username":"mor_2314","password":"<PASSWORD>"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/auth/login' -H 'Content-Type: application/json' -d '{"username":"mor_2314","password":"<PASSWORD>"}'
```

## Expected result
token has an 'exp' (expiry) claim

## Actual result
token has no 'exp' claim and never expires: claims ['iat', 'sub', 'user']

## Test reference
- Test: `tests/api/auth/test_login.py::test_FS_AUTH_003_token_has_an_expiry`
- Failure message: `token has no 'exp' claim and never expires: claims ['iat', 'sub', 'user']`

[← Auth bugs](README.md) · [All bugs](../README.md)
