# Carts: 14 bugs

🔴 Critical 0 · 🟠 High 1 · 🟡 Medium 13 · 🟢 Low 0

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-CARTS-01](BUG-CARTS-01.md) | 🟠 High | P1 | Anyone can create a cart for another user without logging in | `POST /carts` | FS-CARTS-019 | BUG-002 |
| [BUG-CARTS-02](BUG-CARTS-02.md) | 🟡 Medium | P3 | Cart items are {productId, quantity}, not Product objects as documented | `GET /carts/{id}` | FS-CARTS-010 | BUG-008 |
| [BUG-CARTS-03](BUG-CARTS-03.md) | 🟡 Medium | P2 | Get cart 9999 returns 200 'null' instead of 404 | `GET /carts/{id}` | FS-CARTS-011 | BUG-005 |
| [BUG-CARTS-04](BUG-CARTS-04.md) | 🟡 Medium | P2 | Create cart accepted with an empty body | `POST /carts` | FS-CARTS-014 | BUG-006 |
| [BUG-CARTS-05](BUG-CARTS-05.md) | 🟡 Medium | P2 | Create cart accepts an invalid date | `POST /carts` | FS-CARTS-015 | BUG-006 |
| [BUG-CARTS-06](BUG-CARTS-06.md) | 🟡 Medium | P2 | Create cart accepts products that is not a list | `POST /carts` | FS-CARTS-015 | BUG-006 |
| [BUG-CARTS-07](BUG-CARTS-07.md) | 🟡 Medium | P2 | Create cart accepts text as userId | `POST /carts` | FS-CARTS-015 | BUG-006 |
| [BUG-CARTS-08](BUG-CARTS-08.md) | 🟡 Medium | P2 | Create cart accepted for a user that does not exist | `POST /carts` | FS-CARTS-016 | BUG-006 |
| [BUG-CARTS-09](BUG-CARTS-09.md) | 🟡 Medium | P2 | Create cart accepted with a product that does not exist | `POST /carts` | FS-CARTS-017 | BUG-006 |
| [BUG-CARTS-10](BUG-CARTS-10.md) | 🟡 Medium | P2 | Create cart accepts a negative quantity | `POST /carts` | FS-CARTS-018 | BUG-006 |
| [BUG-CARTS-11](BUG-CARTS-11.md) | 🟡 Medium | P2 | Create cart accepts quantity 0 | `POST /carts` | FS-CARTS-018 | BUG-006 |
| [BUG-CARTS-12](BUG-CARTS-12.md) | 🟡 Medium | P2 | Update cart 9999 returns 200 with a made-up cart | `PUT /carts/{id}` | FS-CARTS-022 | BUG-005 |
| [BUG-CARTS-13](BUG-CARTS-13.md) | 🟡 Medium | P2 | Update cart accepts a negative quantity | `PUT /carts/{id}` | FS-CARTS-024 | BUG-006 |
| [BUG-CARTS-14](BUG-CARTS-14.md) | 🟡 Medium | P2 | Delete cart 9999 returns 200 'null' instead of 404 | `DELETE /carts/{id}` | FS-CARTS-026 | BUG-005 |

[← All bugs](../README.md)
