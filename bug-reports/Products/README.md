# Products: 7 bugs

Critical 0 · High 0 · Medium 7 · Low 0

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-PRODUCTS-01](BUG-PRODUCTS-01.md) | 🟠 Medium | P2 | Get a product that does not exist | `GET /products/{id}` | FS-PRODUCTS-005 | BUG-002 |
| [BUG-PRODUCTS-02](BUG-PRODUCTS-02.md) | 🟠 Medium | P2 | Get a product with a non-numeric id | `GET /products/{id}` | FS-PRODUCTS-006 | BUG-002 |
| [BUG-PRODUCTS-03](BUG-PRODUCTS-03.md) | 🟠 Medium | P3 | Create a product with an empty body | `POST /products` | FS-PRODUCTS-008 | BUG-004 |
| [BUG-PRODUCTS-04](BUG-PRODUCTS-04.md) | 🟠 Medium | P2 | Update a product that does not exist | `PUT /products/{id}` | FS-PRODUCTS-011 | BUG-002 |
| [BUG-PRODUCTS-05](BUG-PRODUCTS-05.md) | 🟠 Medium | P2 | Delete a product that does not exist | `DELETE /products/{id}` | FS-PRODUCTS-013 | BUG-002 |
| [BUG-PRODUCTS-06](BUG-PRODUCTS-06.md) | 🟠 Medium | P3 | Create a product with text as price | `POST /products` | FS-PRODUCTS-014 | BUG-004 |
| [BUG-PRODUCTS-07](BUG-PRODUCTS-07.md) | 🟠 Medium | P3 | Create a product with a non-JSON body | `POST /products` | FS-PRODUCTS-018 | BUG-004 |

[← All bugs](../README.md)
