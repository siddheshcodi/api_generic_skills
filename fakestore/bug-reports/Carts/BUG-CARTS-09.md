# BUG-CARTS-09: Create cart accepted with a product that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-09 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /carts` |
| **Test case** | FS-CARTS-017 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create cart with unknown product is rejected. Expected **400/404**. Got HTTP **201**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/carts` and body `{"userId":1,"date":"2026-10-09","products":[{"productId":99999,"quantity":1}]}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/carts' -H 'Content-Type: application/json' -d '{"userId":1,"date":"2026-10-09","products":[{"productId":99999,"quantity":1}]}'
```

## Expected result
400/404

## Actual result
HTTP **201**, body: `{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":99999,"quantity":1}]}`

## Test reference
- Test: `tests/api/carts/test_create_cart.py::test_FS_CARTS_017_create_cart_with_unknown_product_is_rejected`
- Failure message: `product 99999 does not exist, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":99999,"quantity":1}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
