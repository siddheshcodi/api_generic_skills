# BUG-PRODUCTS-06: Create a product with text as price

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-06 |
| **Module** | Products |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /products` |
| **Test case** | FS-PRODUCTS-014 (negative) |
| **Category** | Input validation |
| **Root cause group** | BUG-004: POST /products, /carts and /users return 201 when the request body is empty or invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Create a product with text as price. The API should return **400 (spec: price is a number)**, but it returned HTTP **201**.

## Why it matters
The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/products` with: price: "abc"
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/products' -H 'Content-Type: application/json' -d '{"title":"qa_auto product","price":"abc","description":"created by API test","category":"electronics","image":"https://i.pravatar.cc"}'
```

## Expected result
400 (spec: price is a number)

## Actual result
HTTP **201**, body: `{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}`

## Test reference
- Test: `tests/api/products/test_create_product.py::test_FS_PRODUCTS_014_create_product_with_text_price_returns_400`
- Failure message: `expected 400 for price 'abc' (spec: number), got POST https://fakestoreapi.com/products -> 201: '{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}'`
