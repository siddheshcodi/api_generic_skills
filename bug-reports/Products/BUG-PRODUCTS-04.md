# BUG-PRODUCTS-04: Update a product that does not exist

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-04 |
| **Module** | Products |
| **Severity** | 🟠 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `PUT /products/{id}` |
| **Test case** | FS-PRODUCTS-011 (negative) |
| **Category** | Response contract / error handling |
| **Root cause group** | BUG-002: GET /products/{id} returns 200 with empty body when product does not exist or id is invalid |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Update a product that does not exist. The API should return **400/404**, but it returned HTTP **200**.

## Why it matters
When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist.

## Steps to reproduce
1. Send `PUT https://fakestoreapi.com/products/9999`
2. Check the status code and response body.

```bash
curl -s -X PUT 'https://fakestoreapi.com/products/9999' -H 'Content-Type: application/json' -d '{"title":"qa_auto product","price":13.5,"description":"created by API test","category":"electronics","image":"https://i.pravatar.cc"}'
```

## Expected result
400/404

## Actual result
HTTP **200**, body: `{"id":9999,"title":"qa_auto product","price":13.5,"description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}`

## Test reference
- Test: `tests/api/products/test_update_product.py::test_FS_PRODUCTS_011_update_nonexistent_product_returns_4xx`
- Failure message: `expected 400/404 for unknown id, got PUT https://fakestoreapi.com/products/9999 -> 200: '{"id":9999,"title":"qa_auto product","price":13.5,"description":"created by API test","image":"https://i.pravatar.cc","category":"electronics"}'`
