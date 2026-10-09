# Carts: 7 bugs

Critical 0 · High 0 · Medium 7 · Low 0

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-CARTS-01](BUG-CARTS-01.md) | 🟠 Medium | P3 | Get a single cart matching the documented schema | `GET /carts/{id}` | FS-CARTS-002 | BUG-003 |
| [BUG-CARTS-02](BUG-CARTS-02.md) | 🟠 Medium | P2 | Get a cart that does not exist | `GET /carts/{id}` | FS-CARTS-003 | BUG-002 |
| [BUG-CARTS-03](BUG-CARTS-03.md) | 🟠 Medium | P3 | Create a cart with an empty body | `POST /carts` | FS-CARTS-007 | BUG-004 |
| [BUG-CARTS-04](BUG-CARTS-04.md) | 🟠 Medium | P2 | Update a cart that does not exist | `PUT /carts/{id}` | FS-CARTS-009 | BUG-002 |
| [BUG-CARTS-05](BUG-CARTS-05.md) | 🟠 Medium | P2 | Delete a cart that does not exist | `DELETE /carts/{id}` | FS-CARTS-010 | BUG-002 |
| [BUG-CARTS-06](BUG-CARTS-06.md) | 🟠 Medium | P3 | Create a cart with text as userId | `POST /carts` | FS-CARTS-011 | BUG-004 |
| [BUG-CARTS-07](BUG-CARTS-07.md) | 🟠 Medium | P3 | Create a cart where products is not a list | `POST /carts` | FS-CARTS-012 | BUG-004 |

[← All bugs](../README.md)
