# BUG-CARTS-01: Anyone can create a cart for another user without logging in

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-01 |
| **Module** | Carts |
| **Severity** | 🟠 High |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `POST /carts` |
| **Test case** | FS-CARTS-019 (negative, Security) |
| **Root cause** | BUG-002: Products, carts and users can be created, changed and deleted without logging in |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create cart without login is rejected. Expected **401/403**. Got HTTP **201**.

## Why it matters
Anyone, without logging in, can delete products, delete customer accounts, or create shopping carts in another customer's name. Changing data should only be allowed for logged-in people who own the data or are administrators. Right now any visitor or script could wipe or tamper with the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/carts` and body `{"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/carts' -H 'Content-Type: application/json' -d '{"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}'
```

## Expected result
401/403

## Actual result
HTTP **201**, body: `{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}`

## Test reference
- Test: `tests/api/carts/test_create_cart.py::test_FS_CARTS_019_create_cart_without_login_is_rejected`
- Failure message: `anyone can create a cart for user 1 without logging in: POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}'`

[← Carts bugs](README.md) · [All bugs](../README.md)
