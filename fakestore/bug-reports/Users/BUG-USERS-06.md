# BUG-USERS-06: Create user response returns only an id, not the user

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-06 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-009 (positive, Contract) |
| **Root cause** | BUG-009: POST, PUT and PATCH /users do not return the user record |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create user response returns the user. Expected **201 body is the User (username, email echoed)**. Instead: spec: 201 returns the User; response is {'id': 11} (missing ['username', 'email'])

## Why it matters
After creating or changing a customer account, the system's reply doesn't contain the account: a new account comes back with only a number, and an update comes back without the account number at all. Apps can't confirm what was saved or which account was changed. The reply should contain the full account (without the password).

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` and body `{"username":"qa_auto_x","email":"qa_auto_x@example.com","password":"<PASSWORD>"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"qa_auto_x","email":"qa_auto_x@example.com","password":"<PASSWORD>"}'
```

## Expected result
201 body is the User (username, email echoed)

## Actual result
spec: 201 returns the User; response is {'id': 11} (missing ['username', 'email'])

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_009_create_user_response_returns_the_user`
- Failure message: `spec: 201 returns the User; response is {'id': 11} (missing ['username', 'email'])`

[← Users bugs](README.md) · [All bugs](../README.md)
