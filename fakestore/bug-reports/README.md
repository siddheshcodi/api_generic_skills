# Bug Report — Fake Store API

**Date:** 2026-10-09 · **Environment:** public (https://fakestoreapi.com) · **Framework:** pytest · **Tracker:** manual (local files only, nothing sent anywhere)

## Test summary

| Test runs | Passed | Failed | Skipped | Pass rate | Test cases (positive / negative) |
|---|---|---|---|---|---|
| 115 | 67 | 48 | 0 | 58.3% | 101 (42 / 59) |

| Module | Runs passed | Pass rate | Bugs | Folder |
|---|---|---|---|---|
| Products | 22 / 37 | 59.5% | 15 | [Products/](Products/README.md) |
| Carts | 16 / 30 | 53.3% | 14 | [Carts/](Carts/README.md) |
| Users | 9 / 25 | 36.0% | 16 | [Users/](Users/README.md) |
| Auth | 10 / 13 | 76.9% | 3 | [Auth/](Auth/README.md) |
| Integration | 10 / 10 | 100.0% | 0 | – |

Every failure reproduced 3/3. Normal flows and all 10 integration flows work; most bugs are in security, error handling and input validation.

## Bugs by severity

| 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low | **Total** |
|---|---|---|---|---|
| 3 | 4 | 37 | 4 | **48** |

## All bugs

### Products (15)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-PRODUCTS-01](Products/BUG-PRODUCTS-01.md) | 🟠 High | P1 | Anyone can delete a product without logging in | `DELETE /products/{id}` | FS-PRODUCTS-027 |
| [BUG-PRODUCTS-02](Products/BUG-PRODUCTS-02.md) | 🟡 Medium | P2 | Get product 9999 returns 200 with an empty body instead of 404 | `GET /products/{id}` | FS-PRODUCTS-007 |
| [BUG-PRODUCTS-03](Products/BUG-PRODUCTS-03.md) | 🟡 Medium | P2 | Get product -1 returns 200 with an empty body | `GET /products/{id}` | FS-PRODUCTS-008 |
| [BUG-PRODUCTS-04](Products/BUG-PRODUCTS-04.md) | 🟡 Medium | P2 | Get product 0 returns 200 with an empty body | `GET /products/{id}` | FS-PRODUCTS-008 |
| [BUG-PRODUCTS-05](Products/BUG-PRODUCTS-05.md) | 🟡 Medium | P2 | Get product '1.5' returns 200 empty instead of 400 | `GET /products/{id}` | FS-PRODUCTS-009 |
| [BUG-PRODUCTS-06](Products/BUG-PRODUCTS-06.md) | 🟡 Medium | P2 | Get product 'abc' returns 200 empty instead of 400 | `GET /products/{id}` | FS-PRODUCTS-009 |
| [BUG-PRODUCTS-07](Products/BUG-PRODUCTS-07.md) | 🟡 Medium | P2 | Create product accepted with an empty body | `POST /products` | FS-PRODUCTS-014 |
| [BUG-PRODUCTS-08](Products/BUG-PRODUCTS-08.md) | 🟡 Medium | P2 | Create product accepts an image that is not a URL | `POST /products` | FS-PRODUCTS-015 |
| [BUG-PRODUCTS-09](Products/BUG-PRODUCTS-09.md) | 🟡 Medium | P2 | Create product accepts a negative price | `POST /products` | FS-PRODUCTS-015 |
| [BUG-PRODUCTS-10](Products/BUG-PRODUCTS-10.md) | 🟡 Medium | P2 | Create product accepts text as price | `POST /products` | FS-PRODUCTS-015 |
| [BUG-PRODUCTS-11](Products/BUG-PRODUCTS-11.md) | 🟡 Medium | P2 | Update product 9999 returns 200 with a made-up product | `PUT /products/{id}` | FS-PRODUCTS-020 |
| [BUG-PRODUCTS-12](Products/BUG-PRODUCTS-12.md) | 🟡 Medium | P2 | Update product accepts text as price | `PUT /products/{id}` | FS-PRODUCTS-022 |
| [BUG-PRODUCTS-13](Products/BUG-PRODUCTS-13.md) | 🟡 Medium | P2 | Delete product 9999 returns 200 with an empty body | `DELETE /products/{id}` | FS-PRODUCTS-025 |
| [BUG-PRODUCTS-14](Products/BUG-PRODUCTS-14.md) | 🟢 Low | P3 | Malformed JSON returns an HTML error page instead of JSON | `POST /products` | FS-PRODUCTS-017 |
| [BUG-PRODUCTS-15](Products/BUG-PRODUCTS-15.md) | 🟢 Low | P4 | Responses reveal the server framework (X-Powered-By: Express) | `GET /products/{id}` | FS-PRODUCTS-029 |

### Carts (14)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-CARTS-01](Carts/BUG-CARTS-01.md) | 🟠 High | P1 | Anyone can create a cart for another user without logging in | `POST /carts` | FS-CARTS-019 |
| [BUG-CARTS-02](Carts/BUG-CARTS-02.md) | 🟡 Medium | P3 | Cart items are {productId, quantity}, not Product objects as documented | `GET /carts/{id}` | FS-CARTS-010 |
| [BUG-CARTS-03](Carts/BUG-CARTS-03.md) | 🟡 Medium | P2 | Get cart 9999 returns 200 'null' instead of 404 | `GET /carts/{id}` | FS-CARTS-011 |
| [BUG-CARTS-04](Carts/BUG-CARTS-04.md) | 🟡 Medium | P2 | Create cart accepted with an empty body | `POST /carts` | FS-CARTS-014 |
| [BUG-CARTS-05](Carts/BUG-CARTS-05.md) | 🟡 Medium | P2 | Create cart accepts an invalid date | `POST /carts` | FS-CARTS-015 |
| [BUG-CARTS-06](Carts/BUG-CARTS-06.md) | 🟡 Medium | P2 | Create cart accepts products that is not a list | `POST /carts` | FS-CARTS-015 |
| [BUG-CARTS-07](Carts/BUG-CARTS-07.md) | 🟡 Medium | P2 | Create cart accepts text as userId | `POST /carts` | FS-CARTS-015 |
| [BUG-CARTS-08](Carts/BUG-CARTS-08.md) | 🟡 Medium | P2 | Create cart accepted for a user that does not exist | `POST /carts` | FS-CARTS-016 |
| [BUG-CARTS-09](Carts/BUG-CARTS-09.md) | 🟡 Medium | P2 | Create cart accepted with a product that does not exist | `POST /carts` | FS-CARTS-017 |
| [BUG-CARTS-10](Carts/BUG-CARTS-10.md) | 🟡 Medium | P2 | Create cart accepts a negative quantity | `POST /carts` | FS-CARTS-018 |
| [BUG-CARTS-11](Carts/BUG-CARTS-11.md) | 🟡 Medium | P2 | Create cart accepts quantity 0 | `POST /carts` | FS-CARTS-018 |
| [BUG-CARTS-12](Carts/BUG-CARTS-12.md) | 🟡 Medium | P2 | Update cart 9999 returns 200 with a made-up cart | `PUT /carts/{id}` | FS-CARTS-022 |
| [BUG-CARTS-13](Carts/BUG-CARTS-13.md) | 🟡 Medium | P2 | Update cart accepts a negative quantity | `PUT /carts/{id}` | FS-CARTS-024 |
| [BUG-CARTS-14](Carts/BUG-CARTS-14.md) | 🟡 Medium | P2 | Delete cart 9999 returns 200 'null' instead of 404 | `DELETE /carts/{id}` | FS-CARTS-026 |

### Users (16)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-USERS-01](Users/BUG-USERS-01.md) | 🔴 Critical | P1 | User list returns every user's password without login | `GET /users` | FS-USERS-003 |
| [BUG-USERS-02](Users/BUG-USERS-02.md) | 🔴 Critical | P1 | Single user returns the password without login | `GET /users/{id}` | FS-USERS-007 |
| [BUG-USERS-03](Users/BUG-USERS-03.md) | 🔴 Critical | P1 | Delete user response returns the password | `DELETE /users/{id}` | FS-USERS-021 |
| [BUG-USERS-04](Users/BUG-USERS-04.md) | 🟠 High | P1 | Anyone can delete a user account without logging in | `DELETE /users/{id}` | FS-USERS-024 |
| [BUG-USERS-05](Users/BUG-USERS-05.md) | 🟡 Medium | P2 | Get user 9999 returns 200 'null' instead of 404 | `GET /users/{id}` | FS-USERS-005 |
| [BUG-USERS-06](Users/BUG-USERS-06.md) | 🟡 Medium | P3 | Create user response returns only an id, not the user | `POST /users` | FS-USERS-009 |
| [BUG-USERS-07](Users/BUG-USERS-07.md) | 🟡 Medium | P2 | New users are often given the id of an existing user (id 1) | `POST /users` | FS-USERS-010 |
| [BUG-USERS-08](Users/BUG-USERS-08.md) | 🟡 Medium | P2 | Create user accepted with an empty body | `POST /users` | FS-USERS-011 |
| [BUG-USERS-09](Users/BUG-USERS-09.md) | 🟡 Medium | P2 | Create user accepts an invalid email | `POST /users` | FS-USERS-012 |
| [BUG-USERS-10](Users/BUG-USERS-10.md) | 🟡 Medium | P2 | Create user accepted without a password | `POST /users` | FS-USERS-013 |
| [BUG-USERS-11](Users/BUG-USERS-11.md) | 🟡 Medium | P3 | Create user accepts an existing username | `POST /users` | FS-USERS-014 |
| [BUG-USERS-12](Users/BUG-USERS-12.md) | 🟡 Medium | P3 | PATCH user response has no user id | `PUT, PATCH /users/{id}` | FS-USERS-016 |
| [BUG-USERS-13](Users/BUG-USERS-13.md) | 🟡 Medium | P3 | PUT user response has no user id | `PUT, PATCH /users/{id}` | FS-USERS-016 |
| [BUG-USERS-14](Users/BUG-USERS-14.md) | 🟡 Medium | P2 | Update user 9999 returns 200 instead of 404 | `PUT /users/{id}` | FS-USERS-017 |
| [BUG-USERS-15](Users/BUG-USERS-15.md) | 🟡 Medium | P2 | Update user accepts an invalid email | `PUT /users/{id}` | FS-USERS-019 |
| [BUG-USERS-16](Users/BUG-USERS-16.md) | 🟡 Medium | P2 | Delete user 9999 returns 200 'null' instead of 404 | `DELETE /users/{id}` | FS-USERS-022 |

### Auth (3)

| Bug | Severity | Priority | Title | Endpoint | Test case |
|---|---|---|---|---|---|
| [BUG-AUTH-01](Auth/BUG-AUTH-01.md) | 🟠 High | P2 | Login token never expires (no 'exp' claim) | `POST /auth/login` | FS-AUTH-003 |
| [BUG-AUTH-02](Auth/BUG-AUTH-02.md) | 🟢 Low | P4 | Login returns 201 instead of the documented 200 | `POST /auth/login` | FS-AUTH-001 |
| [BUG-AUTH-03](Auth/BUG-AUTH-03.md) | 🟢 Low | P3 | Login errors are plain text, not JSON | `POST /auth/login` | FS-AUTH-010 |

## Root causes (for developers)

Fixing one root cause closes all the bugs listed next to it.

| Root cause | Severity | Problem | Bugs |
|---|---|---|---|
| BUG-001 | 🔴 Critical | GET /users, GET /users/{id} and DELETE /users/{id} return every user's password in plain text | BUG-USERS-01, BUG-USERS-02, BUG-USERS-03 |
| BUG-002 | 🟠 High | Products, carts and users can be created, changed and deleted without logging in | BUG-PRODUCTS-01, BUG-CARTS-01, BUG-USERS-04 |
| BUG-003 | 🟠 High | POST /auth/login issues tokens that never expire | BUG-AUTH-01 |
| BUG-004 | 🟡 Medium | POST /users gives a new user the id of an existing user (id 1) in about 40% of calls | BUG-USERS-07 |
| BUG-005 | 🟡 Medium | Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 | BUG-PRODUCTS-02, BUG-PRODUCTS-03, BUG-PRODUCTS-04, BUG-PRODUCTS-05, BUG-PRODUCTS-06, BUG-PRODUCTS-11, BUG-PRODUCTS-13, BUG-CARTS-03, BUG-CARTS-12, BUG-CARTS-14, BUG-USERS-05, BUG-USERS-14, BUG-USERS-16 |
| BUG-006 | 🟡 Medium | Create and update accept empty and invalid data for products, carts and users | BUG-PRODUCTS-07, BUG-PRODUCTS-08, BUG-PRODUCTS-09, BUG-PRODUCTS-10, BUG-PRODUCTS-12, BUG-CARTS-04, BUG-CARTS-05, BUG-CARTS-06, BUG-CARTS-07, BUG-CARTS-08, BUG-CARTS-09, BUG-CARTS-10, BUG-CARTS-11, BUG-CARTS-13, BUG-USERS-08, BUG-USERS-09, BUG-USERS-10, BUG-USERS-15 |
| BUG-007 | 🟡 Medium | POST /users accepts a username that already exists | BUG-USERS-11 |
| BUG-008 | 🟡 Medium | GET /carts/{id} products do not match the documented Cart schema | BUG-CARTS-02 |
| BUG-009 | 🟡 Medium | POST, PUT and PATCH /users do not return the user record | BUG-USERS-06, BUG-USERS-12, BUG-USERS-13 |
| BUG-010 | 🟢 Low | Error responses are plain text or HTML pages instead of JSON | BUG-PRODUCTS-14, BUG-AUTH-03 |
| BUG-011 | 🟢 Low | POST /auth/login returns 201 instead of the documented 200 | BUG-AUTH-02 |
| BUG-012 | 🟢 Low | Responses reveal the server framework (X-Powered-By: Express) | BUG-PRODUCTS-15 |

## Files

- `<Module>/README.md`: bug list for that module
- `<Module>/BUG-<MODULE>-NN.md`: one bug: steps, curl, expected vs actual
- `bugs.csv`: all bugs in one sheet (opens in Excel)
- Root-cause bug data (JSON, used for ProofHub later): [../api-test-reports/bugs/](../api-test-reports/bugs/)
- Every test case with its result: [../api-test-reports/test-report.md](../api-test-reports/test-report.md)
