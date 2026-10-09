# BUG-CARTS-11: Create cart accepts quantity 0

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-11 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /carts` |
| **Test case** | FS-CARTS-018 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create cart with invalid quantity returns 400 (id 0). Expected **400**. Got HTTP **201**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/carts` and body `{"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":0}]}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/carts' -H 'Content-Type: application/json' -d '{"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":0}]}'
```

## Expected result
400

## Actual result
HTTP **201**, body: `{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":0}]}`

## Test reference
- Test: `tests/api/carts/test_create_cart.py::test_FS_CARTS_018_create_cart_with_invalid_quantity_returns_400[zero]`
- Failure message: `quantity 0 should be rejected, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":0}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
