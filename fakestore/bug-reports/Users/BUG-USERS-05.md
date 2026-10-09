# BUG-USERS-05: Get user 9999 returns 200 'null' instead of 404

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-05 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `GET /users/{id}` |
| **Test case** | FS-USERS-005 (negative, Error handling) |
| **Root cause** | BUG-005: Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Get nonexistent user returns 4xx. Expected **400/404, not 200 null**. Got HTTP **200**.

## Why it matters
When you ask for, change or delete a product, cart or user that doesn't exist (or use letters instead of a number), the system answers 'OK, success' and sends back nothing - or even pretends to update item 9999. It should clearly say 'not found' or 'invalid number'. Apps relying on it show blank pages or think a change worked when it didn't.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/users/9999`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/users/9999'
```

## Expected result
400/404, not 200 null

## Actual result
HTTP **200**, body: `null`

## Test reference
- Test: `tests/api/users/test_get_user.py::test_FS_USERS_005_get_nonexistent_user_returns_4xx`
- Failure message: `expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/users/9999 -> 200: 'null'`

[← Users bugs](README.md) · [All bugs](../README.md)
