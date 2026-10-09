# BUG-USERS-03: Delete user response returns the password

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-03 |
| **Module** | Users |
| **Severity** | 🔴 Critical |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `DELETE /users/{id}` |
| **Test case** | FS-USERS-021 (negative, Security) |
| **Root cause** | BUG-001: GET /users, GET /users/{id} and DELETE /users/{id} return every user's password in plain text |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Delete response does not expose password. Expected **no 'password' in response**. Instead: DELETE /users/1 response contains the password

## Why it matters
Anyone on the internet, without logging in, can open the user list and read every customer's password in plain text - and those passwords really work to log in. Passwords should never be sent back by the system. With them, a stranger can take over any customer account.

## Steps to reproduce
1. Send `DELETE https://fakestoreapi.com/users/1`
2. Check the status code and response body.

```bash
curl -s -X DELETE 'https://fakestoreapi.com/users/1'
```

## Expected result
no 'password' in response

## Actual result
DELETE /users/1 response contains the password

## Test reference
- Test: `tests/api/users/test_delete_user.py::test_FS_USERS_021_delete_response_does_not_expose_password`
- Failure message: `DELETE /users/1 response contains the password`

[← Users bugs](README.md) · [All bugs](../README.md)
