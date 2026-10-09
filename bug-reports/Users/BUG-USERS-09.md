# BUG-USERS-09: Create a user without a password

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-09 |
| **Module** | Users |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-014 (negative) |
| **Category** | Input validation |
| **Root cause group** | BUG-004: POST /products, /carts and /users return 201 when the request body is empty or invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Create a user without a password. The API should return **400**, but it returned HTTP **201**.

## Why it matters
The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` with: username + email only
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"qa_auto_user","email":"qa_auto_user@example.com"}'
```

## Expected result
400

## Actual result
HTTP **201**, body: `{"id":1}`

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_014_create_user_without_password_returns_400`
- Failure message: `expected 400 when password is missing, got POST https://fakestoreapi.com/users -> 201: '{"id":1}'`
