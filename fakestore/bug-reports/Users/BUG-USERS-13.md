# BUG-USERS-13: PUT user response has no user id

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-13 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `PUT, PATCH /users/{id}` |
| **Test case** | FS-USERS-016 (positive, Contract) |
| **Root cause** | BUG-009: POST, PUT and PATCH /users do not return the user record |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update user response identifies the user (PUT). Expected **200 body is the User incl. id 2**. Instead: spec: 200 returns the User; PUT response has no id: {'username': 'qa_auto_user'}

## Why it matters
After creating or changing a customer account, the system's reply doesn't contain the account: a new account comes back with only a number, and an update comes back without the account number at all. Apps can't confirm what was saved or which account was changed. The reply should contain the full account (without the password).

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/users/2` and body `{"username":"qa_auto_user"}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/users/2' -H 'Content-Type: application/json' -d '{"username":"qa_auto_user"}'
```

## Expected result
200 body is the User incl. id 2

## Actual result
spec: 200 returns the User; PUT response has no id: {'username': 'qa_auto_user'}

## Test reference
- Test: `tests/api/users/test_update_user.py::test_FS_USERS_016_update_user_response_identifies_the_user[PUT]`
- Failure message: `spec: 200 returns the User; PUT response has no id: {'username': 'qa_auto_user'}`

[← Users bugs](README.md) · [All bugs](../README.md)
