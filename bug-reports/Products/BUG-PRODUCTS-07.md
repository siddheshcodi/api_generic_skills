# BUG-PRODUCTS-07: Create a product with a non-JSON body

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-07 |
| **Module** | Products |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /products` |
| **Test case** | FS-PRODUCTS-018 (negative) |
| **Category** | Input validation |
| **Root cause group** | BUG-004: POST /products, /carts and /users return 201 when the request body is empty or invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Create a product with a non-JSON body. The API should return **400/415**, but it returned HTTP **201**.

## Why it matters
The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/products` with: Content-Type text/plain, body title=x
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/products' -H 'Content-Type: text/plain' -d 'title=x'
```

## Expected result
400/415

## Actual result
HTTP **201**, body: `{"id":21}`

## Test reference
- Test: `tests/api/products/test_create_product.py::test_FS_PRODUCTS_018_create_product_with_non_json_body_returns_4xx`
- Failure message: `expected 400/415 for a text/plain body, got POST https://fakestoreapi.com/products -> 201: '{"id":21}'`
