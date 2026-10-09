# BUG-PRODUCTS-14: Malformed JSON returns an HTML error page instead of JSON

| Field | Value |
|---|---|
| **Bug ID** | BUG-PRODUCTS-14 |
| **Module** | Products |
| **Severity** | 🟢 Low |
| **Priority** | P3 |
| **Status** | Open |
| **Endpoint** | `POST /products` |
| **Test case** | FS-PRODUCTS-017 (negative, Contract) |
| **Root cause** | BUG-010: Error responses are plain text or HTML pages instead of JSON |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Malformed json error is returned as json. Expected **error body is JSON, not an HTML page**. Instead: error body is 'text/html; charset=utf-8', not JSON: '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Error</tit'

## Why it matters
When something goes wrong at login (wrong password, missing fields) or the request is badly formed, the system answers with plain text or a web page instead of the structured format it uses everywhere else. Apps can't read these errors reliably and may crash or show raw HTML to the user.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/products` and body `{bad json`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/products' -H 'Content-Type: application/json' -d '{bad json'
```

## Expected result
error body is JSON, not an HTML page

## Actual result
error body is 'text/html; charset=utf-8', not JSON: '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Error</tit'

## Test reference
- Test: `tests/api/products/test_create_product.py::test_FS_PRODUCTS_017_malformed_json_error_is_returned_as_json`
- Failure message: `error body is 'text/html; charset=utf-8', not JSON: '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Error</tit'`

[← Products bugs](README.md) · [All bugs](../README.md)
