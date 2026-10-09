# BUG-PRODUCTS-15: Responses reveal the server framework (X-Powered-By: Express)

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-15 |
| **Module** | Products |
| **Severity** | 🟢 Low |
| **Priority** | P4 |
| **Status** | Open |
| **Endpoint** | `GET /products/{id}` |
| **Test case** | FS-PRODUCTS-029 (negative, Security) |
| **Root cause** | BUG-012: Responses reveal the server framework (X-Powered-By: Express) |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Response does not reveal server framework. Expected **no X-Powered-By header**. Instead: X-Powered-By: Express

## Why it matters
Every reply tells the world which software the server runs on. This doesn't break anything, but it helps attackers pick known weaknesses for that software. The header should be switched off.

## Steps to reproduce
1. Send `GET https://fakestoreapi.com/products/1`
2. Check the status code and response body.

```bash
curl -s -X GET 'https://fakestoreapi.com/products/1'
```

## Expected result
no X-Powered-By header

## Actual result
X-Powered-By: Express

## Test reference
- Test: `tests/api/products/test_transport_security.py::test_FS_PRODUCTS_029_response_does_not_reveal_server_framework`
- Failure message: `X-Powered-By: Express`

[← Products bugs](README.md) · [All bugs](../README.md)
