# BUG-USERS-11: Create user accepts an existing username

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-11 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-014 (negative, Validation) |
| **Root cause** | BUG-007: POST /users accepts a username that already exists |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create user with existing username is rejected. Expected **400/409 duplicate**. Got HTTP **201**.

## Why it matters
A new account can be created with exactly the same username as an existing customer. Usernames are used to log in, so two accounts with the same name means the wrong person could end up logged in. The system should say 'username already taken'.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` and body `{"username":"mor_2314","email":"mor_2314@example.com","password":"<PASSWORD>"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"mor_2314","email":"mor_2314@example.com","password":"<PASSWORD>"}'
```

## Expected result
400/409 duplicate

## Actual result
HTTP **201**, body: `{"id":11}`

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_014_create_user_with_existing_username_is_rejected`
- Failure message: `username 'mor_2314' already exists, got POST https://fakestoreapi.com/users -> 201: '{"id":11}'`

[← Users bugs](README.md) · [All bugs](../README.md)
