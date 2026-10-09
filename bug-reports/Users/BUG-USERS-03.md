# BUG-USERS-03: Single-user responses must not expose password (GET)

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-03 |
| **Module** | Users |
| **Severity** | 🔴 Critical |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `GET /users/{id}` |
| **Test case** | FS-USERS-009 (negative) |
| **Category** | Security - sensitive data exposure |
| **Root cause group** | BUG-001: GET /users returns every user's plaintext password without authentication |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Single-user responses must not expose password. The API should return **no 'password' field in the response**. Instead: GET /users/1 response contains a password field.

## Why it matters
Anyone on the internet, without logging in, can open the user list and see every customer's password in plain readable text. Passwords should never be shown to anyone, and the user list should only be visible to logged-in, authorised people. Right now a stranger can copy any password and log in as that customer.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/users/1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/users/1'
```

## Expected result
no 'password' field in the response

## Actual result
GET /users/1 response contains a password field

200 OK without any token; all users include 'password' in plaintext, e.g. {"id":1,"username":"johnd","password":"<MASKED>",...}. GET /users/{id} and DELETE /users/{id} return it as well.

## Test reference
- Test: `tests/api/users/test_get_user.py::test_FS_USERS_009_single_user_responses_do_not_expose_password[GET]`
- Failure message: `GET /users/1 response contains a password field`
