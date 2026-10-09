# Products: 15 bugs

🔴 Critical 0 · 🟠 High 1 · 🟡 Medium 12 · 🟢 Low 2

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-PRODUCTS-01](BUG-PRODUCTS-01.md) | 🟠 High | P1 | Anyone can delete a product without logging in | `DELETE /products/{id}` | FS-PRODUCTS-027 | BUG-002 |
| [BUG-PRODUCTS-02](BUG-PRODUCTS-02.md) | 🟡 Medium | P2 | Get product 9999 returns 200 with an empty body instead of 404 | `GET /products/{id}` | FS-PRODUCTS-007 | BUG-005 |
| [BUG-PRODUCTS-03](BUG-PRODUCTS-03.md) | 🟡 Medium | P2 | Get product -1 returns 200 with an empty body | `GET /products/{id}` | FS-PRODUCTS-008 | BUG-005 |
| [BUG-PRODUCTS-04](BUG-PRODUCTS-04.md) | 🟡 Medium | P2 | Get product 0 returns 200 with an empty body | `GET /products/{id}` | FS-PRODUCTS-008 | BUG-005 |
| [BUG-PRODUCTS-05](BUG-PRODUCTS-05.md) | 🟡 Medium | P2 | Get product '1.5' returns 200 empty instead of 400 | `GET /products/{id}` | FS-PRODUCTS-009 | BUG-005 |
| [BUG-PRODUCTS-06](BUG-PRODUCTS-06.md) | 🟡 Medium | P2 | Get product 'abc' returns 200 empty instead of 400 | `GET /products/{id}` | FS-PRODUCTS-009 | BUG-005 |
| [BUG-PRODUCTS-07](BUG-PRODUCTS-07.md) | 🟡 Medium | P2 | Create product accepted with an empty body | `POST /products` | FS-PRODUCTS-014 | BUG-006 |
| [BUG-PRODUCTS-08](BUG-PRODUCTS-08.md) | 🟡 Medium | P2 | Create product accepts an image that is not a URL | `POST /products` | FS-PRODUCTS-015 | BUG-006 |
| [BUG-PRODUCTS-09](BUG-PRODUCTS-09.md) | 🟡 Medium | P2 | Create product accepts a negative price | `POST /products` | FS-PRODUCTS-015 | BUG-006 |
| [BUG-PRODUCTS-10](BUG-PRODUCTS-10.md) | 🟡 Medium | P2 | Create product accepts text as price | `POST /products` | FS-PRODUCTS-015 | BUG-006 |
| [BUG-PRODUCTS-11](BUG-PRODUCTS-11.md) | 🟡 Medium | P2 | Update product 9999 returns 200 with a made-up product | `PUT /products/{id}` | FS-PRODUCTS-020 | BUG-005 |
| [BUG-PRODUCTS-12](BUG-PRODUCTS-12.md) | 🟡 Medium | P2 | Update product accepts text as price | `PUT /products/{id}` | FS-PRODUCTS-022 | BUG-006 |
| [BUG-PRODUCTS-13](BUG-PRODUCTS-13.md) | 🟡 Medium | P2 | Delete product 9999 returns 200 with an empty body | `DELETE /products/{id}` | FS-PRODUCTS-025 | BUG-005 |
| [BUG-PRODUCTS-14](BUG-PRODUCTS-14.md) | 🟢 Low | P3 | Malformed JSON returns an HTML error page instead of JSON | `POST /products` | FS-PRODUCTS-017 | BUG-010 |
| [BUG-PRODUCTS-15](BUG-PRODUCTS-15.md) | 🟢 Low | P4 | Responses reveal the server framework (X-Powered-By: Express) | `GET /products/{id}` | FS-PRODUCTS-029 | BUG-012 |

[← All bugs](../README.md)
