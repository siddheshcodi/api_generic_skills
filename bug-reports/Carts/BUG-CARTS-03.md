# BUG-CARTS-03: Create a cart with an empty body

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-03 |
| **Module** | Carts |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /carts` |
| **Test case** | FS-CARTS-007 (negative) |
| **Category** | Input validation |
| **Root cause group** | BUG-004: POST /products, /carts and /users return 201 when the request body is empty or invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Create a cart with an empty body. The API should return **400 (no userId / products)**, but it returned HTTP **201**.

## Why it matters
The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/carts` with: {}
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/carts' -H 'Content-Type: application/json' -d '{}'
```

## Expected result
400 (no userId / products)

## Actual result
HTTP **201**, body: `{"id":11}`

## Test reference
- Test: `tests/api/carts/test_create_cart.py::test_FS_CARTS_007_create_cart_with_empty_body_returns_400`
- Failure message: `expected 400 for empty cart (no userId/products), got POST https://fakestoreapi.com/carts -> 201: '{"id":11}'`
