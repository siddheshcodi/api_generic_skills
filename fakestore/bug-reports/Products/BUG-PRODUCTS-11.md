# BUG-PRODUCTS-11: Update product 9999 returns 200 with a made-up product

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-11 |
| **Module** | Products |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /products/{id}` |
| **Test case** | FS-PRODUCTS-020 (negative, Error handling) |
| **Root cause** | BUG-005: Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update nonexistent product returns 4xx. Expected **400/404**. Got HTTP **200**.

## Why it matters
When you ask for, change or delete a product, cart or user that doesn't exist (or use letters instead of a number), the system answers 'OK, success' and sends back nothing - or even pretends to update item 9999. It should clearly say 'not found' or 'invalid number'. Apps relying on it show blank pages or think a change worked when it didn't.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/products/9999` and body `{"title":"x"}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/products/9999' -H 'Content-Type: application/json' -d '{"title":"x"}'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `{"id":9999,"title":"x"}`

## Test reference
- Test: `tests/api/products/test_update_product.py::test_FS_PRODUCTS_020_update_nonexistent_product_returns_4xx`
- Failure message: `expected 400/404 for unknown/invalid id, got PUT https://fakestoreapi.com/products/9999 -> 200: '{"id":9999,"title":"x"}'`

[← Products bugs](README.md) · [All bugs](../README.md)
