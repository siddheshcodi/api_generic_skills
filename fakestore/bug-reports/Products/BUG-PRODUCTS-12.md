# BUG-PRODUCTS-12: Update product accepts text as price

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-12 |
| **Module** | Products |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /products/{id}` |
| **Test case** | FS-PRODUCTS-022 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update product with text price returns 400. Expected **400**. Got HTTP **200**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/products/1` and body `{"price":"abc"}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/products/1' -H 'Content-Type: application/json' -d '{"price":"abc"}'
```

## Expected result
400

## Actual result
HTTP **200**, body: `{"id":1,"price":"abc"}`

## Test reference
- Test: `tests/api/products/test_update_product.py::test_FS_PRODUCTS_022_update_product_with_text_price_returns_400`
- Failure message: `price 'abc' should be rejected, got PUT https://fakestoreapi.com/products/1 -> 200: '{"id":1,"price":"abc"}'`

[← Products bugs](README.md) · [All bugs](../README.md)
