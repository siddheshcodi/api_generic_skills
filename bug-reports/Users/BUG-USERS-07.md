# BUG-USERS-07: Delete a user that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-07 |
| **Module** | Users |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `DELETE /users/{id}` |
| **Test case** | FS-USERS-012 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Delete a user that does not exist. The API should return **400/404**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `DELETE https://fakestoreapi.com/users/9999`
2. Check the status code and response body.

```bash
curl -s -X DELETE 'https://fakestoreapi.com/users/9999'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `null`

## Test reference
- Test: `tests/api/users/test_delete_user.py::test_FS_USERS_012_delete_nonexistent_user_returns_4xx`
- Failure message: `expected 400/404 for unknown id, got DELETE https://fakestoreapi.com/users/9999 -> 200: 'null'`
