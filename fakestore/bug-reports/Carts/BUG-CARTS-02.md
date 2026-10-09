# BUG-CARTS-02: Cart items are {productId, quantity}, not Product objects as documented

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-02 |
| **Module** | Carts |
| **Severity** | 🟡 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `GET /carts/{id}` |
| **Test case** | FS-CARTS-010 (positive, Contract) |
| **Root cause** | BUG-008: GET /carts/{id} products do not match the documented Cart schema |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Single cart matches spec schema. Expected **matches OpenAPI Cart (products[] are Product)**. Instead: Schema validation error: 'id' is a required property

## Why it matters
The items inside a cart look different from what the API documentation promises. The documentation says each item is a full product (name, price, picture), but the system only sends a product number and a quantity. Developers who follow the documentation build screens that break.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/carts/1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/carts/1'
```

## Expected result
matches OpenAPI Cart (products[] are Product)

## Actual result
Schema validation error: 'id' is a required property

## Test reference
- Test: `tests/api/carts/test_get_cart.py::test_FS_CARTS_010_single_cart_matches_spec_schema`
- Failure message: `Schema validation error: 'id' is a required property`

[← Carts bugs](README.md) · [All bugs](../README.md)
