# BUG-CARTS-01: Get a single cart matching the documented schema

| Field | Value |
|---|---|
| **Bug ID** | BUG-CARTS-01 |
| **Module** | Carts |
| **Severity** | 🟠 Medium |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `GET /carts/{id}` |
| **Test case** | FS-CARTS-002 (positive) |
| **Category** | Response contract |
| **Root cause group** | BUG-003: GET /carts/{id} products items do not match the documented Cart schema |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Get a single cart matching the documented schema. The API should return **200, products[] items are Product objects (per spec)**. Instead: Schema validation error: 'id' is a required property.

## Why it matters
When you open a shopping cart, the list of items inside it looks different from what the API documentation promises. The documentation says each item comes with full product details (name, price, picture), but the system only sends a product number and quantity. Developers who follow the documentation will build screens that break; either the system or the documentation needs to be fixed so they match.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/carts/1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/carts/1'
```

## Expected result
200, products[] items are Product objects (per spec)

## Actual result
Schema validation error: 'id' is a required property

products[] items are {"productId":1,"quantity":4}; extra undocumented fields 'date' and '__v'

## Test reference
- Test: `tests/api/carts/test_get_cart.py::test_FS_CARTS_002_get_single_cart_matches_spec_schema`
- Failure message: `Schema validation error: 'id' is a required property`
