# BUG-USERS-02: Single user returns the password without login

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-02 |
| **Module** | Users |
| **Severity** | 🔴 Critical |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `GET /users/{id}` |
| **Test case** | FS-USERS-007 (negative, Security) |
| **Root cause** | BUG-001: GET /users, GET /users/{id} and DELETE /users/{id} return every user's password in plain text |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Single user does not expose password. Expected **no 'password' field**. Instead: GET /users/1 (no login needed) returns the user's password

## Why it matters
Anyone on the internet, without logging in, can open the user list and read every customer's password in plain text - and those passwords really work to log in. Passwords should never be sent back by the system. With them, a stranger can take over any customer account.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/users/1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/users/1'
```

## Expected result
no 'password' field

## Actual result
GET /users/1 (no login needed) returns the user's password

## Test reference
- Test: `tests/api/users/test_get_user.py::test_FS_USERS_007_single_user_does_not_expose_password`
- Failure message: `GET /users/1 (no login needed) returns the user's password`

[← Users bugs](README.md) · [All bugs](../README.md)
