# BUG-USERS-06: Update a user that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-06 |
| **Module** | Users |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /users/{id}` |
| **Test case** | FS-USERS-011 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Update a user that does not exist. The API should return **400/404**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/users/9999`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/users/9999' -H 'Content-Type: application/json' -d '{"username":"qa_auto_user"}'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `{"username":"qa_auto_2931c1fe"}`

## Test reference
- Test: `tests/api/users/test_update_user.py::test_FS_USERS_011_update_nonexistent_user_returns_4xx`
- Failure message: `expected 400/404 for unknown id, got PUT https://fakestoreapi.com/users/9999 -> 200: '{"username":"qa_auto_2931c1fe"}'`
