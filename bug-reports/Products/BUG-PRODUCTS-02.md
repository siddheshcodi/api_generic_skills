# BUG-PRODUCTS-02: Get a product with a non-numeric id

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-02 |
| **Module** | Products |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `GET /products/{id}` |
| **Test case** | FS-PRODUCTS-006 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Get a product with a non-numeric id. The API should return **400 (spec: id is integer)**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/products/abc`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/products/abc'
```

## Expected result
400 (spec: id is integer)

## Actual result
HTTP **200**, body: `(empty)`

## Test reference
- Test: `tests/api/products/test_get_product.py::test_FS_PRODUCTS_006_get_product_non_numeric_id_returns_400`
- Failure message: `expected 400 for id 'abc' (spec: id is integer), got GET https://fakestoreapi.com/products/abc -> 200: ''`
