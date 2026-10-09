# BUG-USERS-05: Create a user with an invalid email

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-05 |
| **Module** | Users |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-006 (negative) |
| **Category** | Input validation |
| **Root cause group** | BUG-004: POST /products, /carts and /users return 201 when the request body is empty or invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Create a user with an invalid email. The API should return **400**, but it returned HTTP **201**.

## Why it matters
The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` with: email: not-an-email
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"qa_auto_user","email":"not-an-email","password":"Passw0rd!"}'
```

## Expected result
400

## Actual result
HTTP **201**, body: `{"id":11}`

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_006_create_user_with_invalid_email_returns_400`
- Failure message: `expected 400 for email 'not-an-email', got POST https://fakestoreapi.com/users -> 201: '{"id":11}'`
