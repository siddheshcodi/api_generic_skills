# BUG-PRODUCTS-03: Get product -1 returns 200 with an empty body

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-03 |
| **Module** | Products |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `GET /products/{id}` |
| **Test case** | FS-PRODUCTS-008 (negative, Validation) |
| **Root cause** | BUG-005: Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Get product out of range id returns 4xx (negative value). Expected **400/404, not an empty 200**. Got HTTP **200**.

## Why it matters
When you ask for, change or delete a product, cart or user that doesn't exist (or use letters instead of a number), the system answers 'OK, success' and sends back nothing - or even pretends to update item 9999. It should clearly say 'not found' or 'invalid number'. Apps relying on it show blank pages or think a change worked when it didn't.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/products/-1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/products/-1'
```

## Expected result
400/404, not an empty 200

## Actual result
HTTP **200**, body: ``

## Test reference
- Test: `tests/api/products/test_get_product.py::test_FS_PRODUCTS_008_get_product_out_of_range_id_returns_4xx[negative]`
- Failure message: `expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/products/-1 -> 200: ''`

[← Products bugs](README.md) · [All bugs](../README.md)
