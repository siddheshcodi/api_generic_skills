# BUG-PRODUCTS-01: Get a product that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-01 |
| **Module** | Products |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `GET /products/{id}` |
| **Test case** | FS-PRODUCTS-005 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Get a product that does not exist. The API should return **400/404, not an empty 200**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/products/9999`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/products/9999'
```

## Expected result
400/404, not an empty 200

## Actual result
HTTP **200**, body: `(empty)`

## Test reference
- Test: `tests/api/products/test_get_product.py::test_FS_PRODUCTS_005_get_nonexistent_product_is_not_empty_200`
- Failure message: `expected 400/404 for unknown id, got GET https://fakestoreapi.com/products/9999 -> 200: ''`
