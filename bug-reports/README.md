# Bug Report — Fake Store API (demo)

**Date:** 2026-10-09 · **Environment:** public (https://fakestoreapi.com) · **Framework:** pytest · **Tracker:** manual (local files only, nothing sent anywhere)

## Test summary

| Total tests | Passed | Failed | Skipped | Pass rate |
|---|---|---|---|---|
| 60 | 36 | 24 | 0 | 60.0% |

| Module | Tests passed | Pass rate | Bugs | Folder |
|---|---|---|---|---|
| Products | 11 / 18 | 61.1% | 7 | [Products/](Products/README.md) |
| Carts | 5 / 12 | 41.7% | 7 | [Carts/](Carts/README.md) |
| Users | 6 / 14 | 42.9% | 9 | [Users/](Users/README.md) |
| Auth | 7 / 8 | 87.5% | 1 | [Auth/](Auth/README.md) |
| Integration | 7 / 7 | 100.0% | 0 | – |

Every failure reproduced 3/3. Normal flows work; the API fails most negative checks (bad input, unknown IDs).

## Bugs by severity

| 🔴 Critical | 🔴 High | 🟠 Medium | 🟢 Low | **Total** |
|---|---|---|---|---|
| 3 | 0 | 20 | 1 | **24** |

## All bugs

### Products (7)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-PRODUCTS-01](Products/BUG-PRODUCTS-01.md) | 🟠 Medium | P2 | Get a product that does not exist | `GET /products/{id}` | FS-PRODUCTS-005 |
| [BUG-PRODUCTS-02](Products/BUG-PRODUCTS-02.md) | 🟠 Medium | P2 | Get a product with a non-numeric id | `GET /products/{id}` | FS-PRODUCTS-006 |
| [BUG-PRODUCTS-03](Products/BUG-PRODUCTS-03.md) | 🟠 Medium | P3 | Create a product with an empty body | `POST /products` | FS-PRODUCTS-008 |
| [BUG-PRODUCTS-04](Products/BUG-PRODUCTS-04.md) | 🟠 Medium | P2 | Update a product that does not exist | `PUT /products/{id}` | FS-PRODUCTS-011 |
| [BUG-PRODUCTS-05](Products/BUG-PRODUCTS-05.md) | 🟠 Medium | P2 | Delete a product that does not exist | `DELETE /products/{id}` | FS-PRODUCTS-013 |
| [BUG-PRODUCTS-06](Products/BUG-PRODUCTS-06.md) | 🟠 Medium | P3 | Create a product with text as price | `POST /products` | FS-PRODUCTS-014 |
| [BUG-PRODUCTS-07](Products/BUG-PRODUCTS-07.md) | 🟠 Medium | P3 | Create a product with a non-JSON body | `POST /products` | FS-PRODUCTS-018 |

### Carts (7)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-CARTS-01](Carts/BUG-CARTS-01.md) | 🟠 Medium | P3 | Get a single cart matching the documented schema | `GET /carts/{id}` | FS-CARTS-002 |
| [BUG-CARTS-02](Carts/BUG-CARTS-02.md) | 🟠 Medium | P2 | Get a cart that does not exist | `GET /carts/{id}` | FS-CARTS-003 |
| [BUG-CARTS-03](Carts/BUG-CARTS-03.md) | 🟠 Medium | P3 | Create a cart with an empty body | `POST /carts` | FS-CARTS-007 |
| [BUG-CARTS-04](Carts/BUG-CARTS-04.md) | 🟠 Medium | P2 | Update a cart that does not exist | `PUT /carts/{id}` | FS-CARTS-009 |
| [BUG-CARTS-05](Carts/BUG-CARTS-05.md) | 🟠 Medium | P2 | Delete a cart that does not exist | `DELETE /carts/{id}` | FS-CARTS-010 |
| [BUG-CARTS-06](Carts/BUG-CARTS-06.md) | 🟠 Medium | P3 | Create a cart with text as userId | `POST /carts` | FS-CARTS-011 |
| [BUG-CARTS-07](Carts/BUG-CARTS-07.md) | 🟠 Medium | P3 | Create a cart where products is not a list | `POST /carts` | FS-CARTS-012 |

### Users (9)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-USERS-01](Users/BUG-USERS-01.md) | 🔴 Critical | P1 | User list must not expose passwords | `GET /users` | FS-USERS-003 |
| [BUG-USERS-02](Users/BUG-USERS-02.md) | 🔴 Critical | P1 | Single-user responses must not expose password (DELETE) | `DELETE /users/{id}` | FS-USERS-009 |
| [BUG-USERS-03](Users/BUG-USERS-03.md) | 🔴 Critical | P1 | Single-user responses must not expose password (GET) | `GET /users/{id}` | FS-USERS-009 |
| [BUG-USERS-04](Users/BUG-USERS-04.md) | 🟠 Medium | P2 | Get a user that does not exist | `GET /users/{id}` | FS-USERS-004 |
| [BUG-USERS-05](Users/BUG-USERS-05.md) | 🟠 Medium | P3 | Create a user with an invalid email | `POST /users` | FS-USERS-006 |
| [BUG-USERS-06](Users/BUG-USERS-06.md) | 🟠 Medium | P2 | Update a user that does not exist | `PUT /users/{id}` | FS-USERS-011 |
| [BUG-USERS-07](Users/BUG-USERS-07.md) | 🟠 Medium | P2 | Delete a user that does not exist | `DELETE /users/{id}` | FS-USERS-012 |
| [BUG-USERS-08](Users/BUG-USERS-08.md) | 🟠 Medium | P3 | Create a user with an empty body | `POST /users` | FS-USERS-013 |
| [BUG-USERS-09](Users/BUG-USERS-09.md) | 🟠 Medium | P3 | Create a user without a password | `POST /users` | FS-USERS-014 |

### Auth (1)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-AUTH-01](Auth/BUG-AUTH-01.md) | 🟢 Low | P4 | Login with valid credentials | `POST /auth/login` | FS-AUTH-001 |

## Root causes (for developers)

Many bugs above share one underlying problem. Fixing a root cause closes all its bugs.

| Root cause | Severity | Problem | Bugs |
|---|---|---|---|
| BUG-001 | 🔴 Critical | GET /users returns every user's plaintext password without authentication | BUG-USERS-01, BUG-USERS-02, BUG-USERS-03 |
| BUG-002 | 🟠 Medium | GET /products/{id} returns 200 with empty body when product does not exist or id is invalid | BUG-PRODUCTS-01, BUG-PRODUCTS-02, BUG-PRODUCTS-04, BUG-PRODUCTS-05, BUG-CARTS-02, BUG-CARTS-04, BUG-CARTS-05, BUG-USERS-04, BUG-USERS-06, BUG-USERS-07 |
| BUG-003 | 🟠 Medium | GET /carts/{id} products items do not match the documented Cart schema | BUG-CARTS-01 |
| BUG-004 | 🟠 Medium | POST /products, /carts and /users return 201 when the request body is empty or invalid | BUG-PRODUCTS-03, BUG-PRODUCTS-06, BUG-PRODUCTS-07, BUG-CARTS-03, BUG-CARTS-06, BUG-CARTS-07, BUG-USERS-05, BUG-USERS-08, BUG-USERS-09 |
| BUG-005 | 🟢 Low | POST /auth/login returns 201 instead of documented 200 on success | BUG-AUTH-01 |

## Files

- `<Module>/README.md`: bug list for that module
- `<Module>/BUG-<MODULE>-NN.md`: one bug: steps, curl, expected vs actual
- `bugs.csv`: all bugs in one sheet (opens in Excel)
- Full test results: [../api-test-reports/test-report.md](../api-test-reports/test-report.md)
