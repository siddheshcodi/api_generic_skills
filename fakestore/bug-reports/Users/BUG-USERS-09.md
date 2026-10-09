# BUG-USERS-09: Create user accepts an invalid email

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-09 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-012 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create user with invalid email returns 400. Expected **400**. Got HTTP **201**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` and body `{"username":"qa_auto_x","email":"not-an-email","password":"<PASSWORD>"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"qa_auto_x","email":"not-an-email","password":"<PASSWORD>"}'
```

## Expected result
400

## Actual result
HTTP **201**, body: `{"id":11}`

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_012_create_user_with_invalid_email_returns_400`
- Failure message: `email 'not-an-email' should be rejected, got POST https://fakestoreapi.com/users -> 201: '{"id":11}'`

[← Users bugs](README.md) · [All bugs](../README.md)
