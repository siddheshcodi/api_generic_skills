# BUG-PRODUCTS-10: Create product accepts text as price

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-10 |
| **Module** | Products |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /products` |
| **Test case** | FS-PRODUCTS-015 (negative, Validation) |
| **Root cause** | BUG-006: Create and update accept empty and invalid data for products, carts and users |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Create product with invalid field returns 400 (text price). Expected **400 (spec: number, uri)**. Got HTTP **201**.

## Why it matters
The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/products` and body `{"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/products' -H 'Content-Type: application/json' -d '{"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}'
```

## Expected result
400 (spec: number, uri)

## Actual result
HTTP **201**, body: `{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}`

## Test reference
- Test: `tests/api/products/test_create_product.py::test_FS_PRODUCTS_015_create_product_with_invalid_field_returns_400[text_price]`
- Failure message: `price='abc' should be rejected, got POST https://fakestoreapi.com/products -> 201: '{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}'`

[← Products bugs](README.md) · [All bugs](../README.md)
