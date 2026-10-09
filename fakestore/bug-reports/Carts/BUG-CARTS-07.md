# BUG-CARTS-07: Create cart accepts text as userId

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-07 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /carts` |
| **Test case** | FS-CARTS-015 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create cart with wrong types returns 400 (text userId). Expected **400**. Got HTTP **201**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/carts` and body `{"userId":"abc","date":"2026-10-09","products":[{"productId":1,"quantity":2}]}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/carts' -H 'Content-Type: application/json' -d '{"userId":"abc","date":"2026-10-09","products":[{"productId":1,"quantity":2}]}'
```

## Expected result
400

## Actual result
HTTP **201**, body: `{"id":11,"userId":"abc","date":"2026-10-09","products":[{"productId":1,"quantity":2}]}`

## Test reference
- Test: `tests/api/carts/test_create_cart.py::test_FS_CARTS_015_create_cart_with_wrong_types_returns_400[text_user_id]`
- Failure message: `{'userId': 'abc'} should be rejected, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":"abc","date":"2026-10-09","products":[{"productId":1,"quantity":2}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
