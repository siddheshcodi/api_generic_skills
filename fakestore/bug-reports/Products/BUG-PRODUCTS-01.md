# BUG-PRODUCTS-01: Anyone can delete a product without logging in

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-01 |
| **Module** | Products |
| **Severity** | 🟠 High |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `DELETE /products/{id}` |
| **Test case** | FS-PRODUCTS-027 (negative, Security) |
| **Root cause** | BUG-002: Products, carts and users can be created, changed and deleted without logging in |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Delete product without login is rejected. Expected **401/403**. Got HTTP **200**.

## Why it matters
Anyone, without logging in, can delete products, delete customer accounts, or create shopping carts in another customer's name. Changing data should only be allowed for logged-in people who own the data or are administrators. Right now any visitor or script could wipe or tamper with the store.

## Steps to reproduce
1. Send `DELETE https://fakestoreapi.com/products/1`
2. Check the status code and response body.

```bash
curl -s -X DELETE 'https://fakestoreapi.com/products/1'
```

## Expected result
401/403

## Actual result
HTTP **200**, body: `{"id":1,"title":"Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops","price":109.95,"description":"Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in`

## Test reference
- Test: `tests/api/products/test_delete_product.py::test_FS_PRODUCTS_027_delete_product_without_login_is_rejected`
- Failure message: `anyone can delete a product without logging in: DELETE https://fakestoreapi.com/products/1 -> 200: '{"id":1,"title":"Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops","price":109.95,"description":"Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in'`

[← Products bugs](README.md) · [All bugs](../README.md)
