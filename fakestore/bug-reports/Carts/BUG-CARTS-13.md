# BUG-CARTS-13: Update cart accepts a negative quantity

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-13 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /carts/{id}` |
| **Test case** | FS-CARTS-024 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Update cart with negative quantity returns 400. Expected **400**. Got HTTP **200**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/carts/1` and body `{"userId":1,"products":[{"productId":1,"quantity":-5}]}`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/carts/1' -H 'Content-Type: application/json' -d '{"userId":1,"products":[{"productId":1,"quantity":-5}]}'
```

## Expected result
400

## Actual result
HTTP **200**, body: `{"id":1,"userId":1,"products":[{"productId":1,"quantity":-5}]}`

## Test reference
- Test: `tests/api/carts/test_update_cart.py::test_FS_CARTS_024_update_cart_with_negative_quantity_returns_400`
- Failure message: `quantity -5 should be rejected, got PUT https://fakestoreapi.com/carts/1 -> 200: '{"id":1,"userId":1,"products":[{"productId":1,"quantity":-5}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
