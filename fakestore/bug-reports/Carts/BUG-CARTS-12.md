# BUG-CARTS-12: Update cart 9999 returns 200 with a made-up cart

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-12 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /carts/{id}` |
| **Test case** | FS-CARTS-022 (negative, Error handling) |
| **Root cause** | BUG-005: Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update nonexistent cart returns 4xx. Expected **400/404**. Got HTTP **200**.

## Why it matters
When you ask for, change or delete a product, cart or user that doesn't exist (or use letters instead of a number), the system answers 'OK, success' and sends back nothing - or even pretends to update item 9999. It should clearly say 'not found' or 'invalid number'. Apps relying on it show blank pages or think a change worked when it didn't.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/carts/9999` and body `{"userId":1,"products":[{"productId":1,"quantity":1}]}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/carts/9999' -H 'Content-Type: application/json' -d '{"userId":1,"products":[{"productId":1,"quantity":1}]}'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `{"id":9999,"userId":1,"products":[{"productId":1,"quantity":1}]}`

## Test reference
- Test: `tests/api/carts/test_update_cart.py::test_FS_CARTS_022_update_nonexistent_cart_returns_4xx`
- Failure message: `expected 400/404 for unknown/invalid id, got PUT https://fakestoreapi.com/carts/9999 -> 200: '{"id":9999,"userId":1,"products":[{"productId":1,"quantity":1}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
