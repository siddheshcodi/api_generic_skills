# BUG-USERS-01: User list returns every user's password without login

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-01 |
| **Module** | Users |
| **Severity** | 🔴 Critical |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `GET /users` |
| **Test case** | FS-USERS-003 (negative, Security) |
| **Root cause** | BUG-001: GET /users, GET /users/{id} and DELETE /users/{id} return every user's password in plain text |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: User list does not expose passwords. Expected **no 'password' field**. Instead: GET /users (no login needed) returns 'password' for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

## Why it matters
Anyone on the internet, without logging in, can open the user list and read every customer's password in plain text - and those passwords really work to log in. Passwords should never be sent back by the system. With them, a stranger can take over any customer account.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/users`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/users'
```

## Expected result
no 'password' field

## Actual result
GET /users (no login needed) returns 'password' for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

## Test reference
- Test: `tests/api/users/test_list_users.py::test_FS_USERS_003_user_list_does_not_expose_passwords`
- Failure message: `GET /users (no login needed) returns 'password' for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`

[← Users bugs](README.md) · [All bugs](../README.md)
