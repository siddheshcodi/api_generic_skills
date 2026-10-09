# BUG-CARTS-05: Delete a cart that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-05 |
| **Module** | Carts |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `DELETE /carts/{id}` |
| **Test case** | FS-CARTS-010 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Delete a cart that does not exist. The API should return **400/404**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `DELETE https://fakestoreapi.com/carts/9999`
2. Check the status code and response body.

```bash
curl -s -X DELETE 'https://fakestoreapi.com/carts/9999'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `null`

## Test reference
- Test: `tests/api/carts/test_delete_cart.py::test_FS_CARTS_010_delete_nonexistent_cart_returns_4xx`
- Failure message: `expected 400/404 for unknown id, got DELETE https://fakestoreapi.com/carts/9999 -> 200: 'null'`
