# BUG-USERS-15: Update user accepts an invalid email

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-15 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /users/{id}` |
| **Test case** | FS-USERS-019 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update user with invalid email returns 400. Expected **400**. Got HTTP **200**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/users/2` and body `{"email":"bad"}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/users/2' -H 'Content-Type: application/json' -d '{"email":"bad"}'
```

## Expected result
400

## Actual result
HTTP **200**, body: `{"email":"bad"}`

## Test reference
- Test: `tests/api/users/test_update_user.py::test_FS_USERS_019_update_user_with_invalid_email_returns_400`
- Failure message: `email 'bad' should be rejected, got PUT https://fakestoreapi.com/users/2 -> 200: '{"email":"bad"}'`

[← Users bugs](README.md) · [All bugs](../README.md)
