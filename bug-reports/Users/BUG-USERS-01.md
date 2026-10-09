# BUG-USERS-01: User list must not expose passwords

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-01 |
| **Module** | Users |
| **Severity** | 🔴 Critical |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `GET /users` |
| **Test case** | FS-USERS-003 (negative) |
| **Category** | Security - sensitive data exposure |
| **Root cause group** | BUG-001: GET /users returns every user's plaintext password without authentication |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
User list must not expose passwords. The API should return **no 'password' field in any user**. Instead: GET /users returns a password field for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (no auth needed).

## Why it matters
Anyone on the internet, without logging in, can open the user list and see every customer's password in plain readable text. Passwords should never be shown to anyone, and the user list should only be visible to logged-in, authorised people. Right now a stranger can copy any password and log in as that customer.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/users` with: no auth
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/users'
```

## Expected result
no 'password' field in any user

## Actual result
GET /users returns a password field for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (no auth needed)

200 OK without any token; all users include 'password' in plaintext, e.g. {"id":1,"username":"johnd","password":"<MASKED>",...}. GET /users/{id} and DELETE /users/{id} return it as well.

## Test reference
- Test: `tests/api/users/test_list_users.py::test_FS_USERS_003_user_responses_do_not_expose_passwords`
- Failure message: `GET /users returns a password field for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (no auth needed)`
