# API Test Report — Fake Store API (demo)

Environment: public (https://fakestoreapi.com) · Source: docs/openapi.json (OpenAPI 3.1 from /docs-data) · Date: 2026-10-09

## 1. Overall result

| Total | Passed | Failed | Errors | Skipped | Not run | Pass rate |
|---|---|---|---|---|---|---|
| 59 | 36 | 23 | 0 | 0 | 0 | 61.0% |

| Scenario type | Total | Passed | Failed | Pass rate |
|---|---|---|---|---|
| Positive | 26 | 24 | 2 | 92.3% |
| Negative | 33 | 12 | 21 | 36.4% |

Bugs: Critical 1 · Medium 3 · Low 1 (total 5)

## 2. Module summary

| Module | Endpoints | Positive | Negative | Total | Passed | Failed | Pass rate | Bugs |
|---|---|---|---|---|---|---|---|---|
| Products | 5 | 7 | 11 | 18 | 11 | 7 | 61.1% | BUG-002, BUG-004 |
| Carts | 5 | 5 | 7 | 12 | 5 | 7 | 41.7% | BUG-002, BUG-003, BUG-004 |
| Users | 6 | 5 | 9 | 14 | 6 | 8 | 42.9% | BUG-001, BUG-002, BUG-004 |
| Auth | 1 | 2 | 6 | 8 | 7 | 1 | 87.5% | BUG-005 |
| Integration | 7 | 7 | 0 | 7 | 7 | 0 | 100.0% | – |

## 3. Module details

### Products — 11/18 passed

Product catalogue: list, filter, read, create, update, delete.

#### Positive scenarios (7)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-001 | List all products | `GET /products` | 200, JSON list, every item matches Product schema | ✅ Pass |  |  |
| FS-PRODUCTS-002 | Limit the number of products | `GET /products` | 200 with exactly 5 items | ✅ Pass |  |  |
| FS-PRODUCTS-003 | Sort products descending | `GET /products` | 200, ids in descending order | ✅ Pass |  |  |
| FS-PRODUCTS-004 | Get a single product | `GET /products/{id}` | 200, Product with id 1 | ✅ Pass |  |  |
| FS-PRODUCTS-007 | Create a product with valid data | `POST /products` | 201, id returned, fields echoed | ✅ Pass |  |  |
| FS-PRODUCTS-010 | Update a product | `PUT /products/{id}` | 200, title updated | ✅ Pass |  |  |
| FS-PRODUCTS-012 | Delete a product | `DELETE /products/{id}` | 200 | ✅ Pass |  |  |

#### Negative scenarios (11)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-005 | Get a product that does not exist | `GET /products/{id}` | 400/404, not an empty 200 | ❌ Fail | expected 400/404 for unknown id, got GET https://fakestoreapi.com/products/9999 -> 200: '' | BUG-002 |
| FS-PRODUCTS-006 | Get a product with a non-numeric id | `GET /products/{id}` | 400 (spec: id is integer) | ❌ Fail | expected 400 for id 'abc' (spec: id is integer), got GET https://fakestoreapi.com/products/abc -> 200: '' | BUG-002 |
| FS-PRODUCTS-008 | Create a product with an empty body | `POST /products` | 400 (request body is required) | ❌ Fail | expected 400 for empty body (requestBody required), got POST https://fakestoreapi.com/products -> 201: '{"id":21}' | BUG-004 |
| FS-PRODUCTS-009 | Create a product with malformed JSON | `POST /products` | 400, never 5xx | ✅ Pass |  |  |
| FS-PRODUCTS-011 | Update a product that does not exist | `PUT /products/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got PUT https://fakestoreapi.com/products/9999 -> 200: '{"id":9999,"title":"qa_auto product","price":13.5,"description":"created by API test","image":"https://i.pravatar.cc","category":"e | BUG-002 |
| FS-PRODUCTS-013 | Delete a product that does not exist | `DELETE /products/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got DELETE https://fakestoreapi.com/products/9999 -> 200: '' | BUG-002 |
| FS-PRODUCTS-014 | Create a product with text as price | `POST /products` | 400 (spec: price is a number) | ❌ Fail | expected 400 for price 'abc' (spec: number), got POST https://fakestoreapi.com/products -> 201: '{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","categ | BUG-004 |
| FS-PRODUCTS-015 | Create a product with a 10,000-character title | `POST /products` | no 5xx (spec sets no max length; 400/413 preferred) | ✅ Pass |  |  |
| FS-PRODUCTS-016 | Update a product with a non-numeric id | `PUT /products/{id}` | 400 | ✅ Pass |  |  |
| FS-PRODUCTS-017 | Delete a product with a non-numeric id | `DELETE /products/{id}` | 400 | ✅ Pass |  |  |
| FS-PRODUCTS-018 | Create a product with a non-JSON body | `POST /products` | 400/415 | ❌ Fail | expected 400/415 for a text/plain body, got POST https://fakestoreapi.com/products -> 201: '{"id":21}' | BUG-004 |

### Carts — 5/12 passed

Shopping carts of users: list, read, create, update, delete.

#### Positive scenarios (5)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-CARTS-001 | List all carts | `GET /carts` | 200, non-empty list | ✅ Pass |  |  |
| FS-CARTS-002 | Get a single cart matching the documented schema | `GET /carts/{id}` | 200, products[] items are Product objects (per spec) | ❌ Fail | jsonschema.exceptions.ValidationError: 'id' is a required property | BUG-003 |
| FS-CARTS-004 | Create a cart | `POST /carts` | 201 with id | ✅ Pass |  |  |
| FS-CARTS-005 | Update a cart | `PUT /carts/{id}` | 200, products updated | ✅ Pass |  |  |
| FS-CARTS-006 | Delete a cart | `DELETE /carts/{id}` | 200 | ✅ Pass |  |  |

#### Negative scenarios (7)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-CARTS-003 | Get a cart that does not exist | `GET /carts/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown id, got GET https://fakestoreapi.com/carts/9999 -> 200: 'null' | BUG-002 |
| FS-CARTS-007 | Create a cart with an empty body | `POST /carts` | 400 (no userId / products) | ❌ Fail | expected 400 for empty cart (no userId/products), got POST https://fakestoreapi.com/carts -> 201: '{"id":11}' | BUG-004 |
| FS-CARTS-008 | Get a cart with a non-numeric id | `GET /carts/{id}` | 400 | ✅ Pass |  |  |
| FS-CARTS-009 | Update a cart that does not exist | `PUT /carts/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got PUT https://fakestoreapi.com/carts/9999 -> 200: '{"id":9999,"userId":1,"products":[{"productId":1,"quantity":1}]}' | BUG-002 |
| FS-CARTS-010 | Delete a cart that does not exist | `DELETE /carts/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got DELETE https://fakestoreapi.com/carts/9999 -> 200: 'null' | BUG-002 |
| FS-CARTS-011 | Create a cart with text as userId | `POST /carts` | 400 (spec: integer) | ❌ Fail | expected 400 for userId 'abc' (spec: integer), got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":"abc","products":[]}' | BUG-004 |
| FS-CARTS-012 | Create a cart where products is not a list | `POST /carts` | 400 (spec: array) | ❌ Fail | expected 400 for products 'x' (spec: array), got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"products":"x"}' | BUG-004 |

### Users — 6/14 passed

Customer accounts: list, read, create, update, delete. Includes sensitive-data checks.

#### Positive scenarios (5)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-USERS-001 | List all users | `GET /users` | 200, every item matches User schema | ✅ Pass |  |  |
| FS-USERS-002 | Get a single user | `GET /users/{id}` | 200, User object | ✅ Pass |  |  |
| FS-USERS-005 | Create a user with valid data | `POST /users` | 201 with id | ✅ Pass |  |  |
| FS-USERS-007 | Update a user | `PUT /users/{id}` | 200, username updated | ✅ Pass |  |  |
| FS-USERS-008 | Delete a user | `DELETE /users/{id}` | 200 | ✅ Pass |  |  |

#### Negative scenarios (9)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-USERS-003 | User list must not expose passwords | `GET /users` | no 'password' field in any user | ❌ Fail | GET /users returns a password field for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (no auth needed) | BUG-001 |
| FS-USERS-004 | Get a user that does not exist | `GET /users/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown id, got GET https://fakestoreapi.com/users/9999 -> 200: 'null' | BUG-002 |
| FS-USERS-006 | Create a user with an invalid email | `POST /users` | 400 | ❌ Fail | expected 400 for email 'not-an-email', got POST https://fakestoreapi.com/users -> 201: '{"id":1}' | BUG-004 |
| FS-USERS-009 | Single-user responses must not expose password | `GET, DELETE /users/{id}` | no 'password' field in the response | ❌ Fail | GET /users/1 response contains a password field | BUG-001 |
| FS-USERS-010 | Get a user with a non-numeric id | `GET /users/{id}` | 400 | ✅ Pass |  |  |
| FS-USERS-011 | Update a user that does not exist | `PUT /users/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got PUT https://fakestoreapi.com/users/9999 -> 200: '{"username":"qa_auto_ecb01b4e"}' | BUG-002 |
| FS-USERS-012 | Delete a user that does not exist | `DELETE /users/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown id, got DELETE https://fakestoreapi.com/users/9999 -> 200: 'null' | BUG-002 |
| FS-USERS-013 | Create a user with an empty body | `POST /users` | 400 | ❌ Fail | expected 400 for empty body, got POST https://fakestoreapi.com/users -> 201: '{"id":11}' | BUG-004 |
| FS-USERS-014 | Create a user without a password | `POST /users` | 400 | ❌ Fail | expected 400 when password is missing, got POST https://fakestoreapi.com/users -> 201: '{"id":1}' | BUG-004 |

### Auth — 7/8 passed

Login that returns a token.

#### Positive scenarios (2)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-AUTH-001 | Login with valid credentials | `POST /auth/login` | 200 + token (per spec) | ❌ Fail | spec documents 200 LoginResponse, got 201 | BUG-005 |
| FS-AUTH-008 | Login token is a well-formed JWT | `POST /auth/login` | token has 3 non-empty parts (header.payload.signature) | ✅ Pass |  |  |

#### Negative scenarios (6)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-AUTH-002 | Login with a wrong password | `POST /auth/login` | 401 | ✅ Pass |  |  |
| FS-AUTH-003 | Login with an empty body | `POST /auth/login` | 400 | ✅ Pass |  |  |
| FS-AUTH-004 | Login with SQL-injection-like input | `POST /auth/login` | 400/401, no 5xx, no token | ✅ Pass |  |  |
| FS-AUTH-005 | Login with an unknown username | `POST /auth/login` | 401 | ✅ Pass |  |  |
| FS-AUTH-006 | Login without a password | `POST /auth/login` | 400 | ✅ Pass |  |  |
| FS-AUTH-007 | Login with numbers instead of text | `POST /auth/login` | 400/401, no token | ✅ Pass |  |  |

### Integration — 7/7 passed

Cross-module flows and data consistency between Auth, Users, Carts and Products (read-only, because this API does not save writes).

#### Positive scenarios (7)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-INTEG-001 | Logged-in user has a profile and their own carts | `POST /auth/login → GET /users → GET /carts` | login gives token; user found in /users; at least one cart with that userId | ✅ Pass |  |  |
| FS-INTEG-002 | Every product in any cart exists in the catalogue | `GET /carts → GET /products` | every cart productId is a real product id | ✅ Pass |  |  |
| FS-INTEG-003 | Every cart belongs to an existing user | `GET /carts → GET /users` | every cart userId is a real user id | ✅ Pass |  |  |
| FS-INTEG-004 | Product list and product detail return the same data | `GET /products → GET /products/{id}` | detail equals the list item for each product | ✅ Pass |  |  |
| FS-INTEG-005 | Login token identifies the same user | `POST /auth/login → GET /users` | token 'sub' claim equals that user's id in /users | ✅ Pass |  |  |
| FS-INTEG-006 | User list and user detail return the same data | `GET /users → GET /users/{id}` | detail equals the list item for each user | ✅ Pass |  |  |
| FS-INTEG-007 | Cart list and cart detail return the same data | `GET /carts → GET /carts/{id}` | detail equals the list item for each cart | ✅ Pass |  |  |

## 4. Bugs found

| Bug | Severity | Title | In simple words | Failed tests | Status |
|---|---|---|---|---|---|
| BUG-001 | Critical | GET /users returns every user's plaintext password without authentication | Anyone on the internet, without logging in, can open the user list and see every customer's password in plain readable text. Passwords should never be shown to anyone, and the user list should only be visible to logged-in, authorised people. Right now a stranger can copy any password and log in as that customer. | FS-USERS-003, FS-USERS-009 | draft |
| BUG-002 | Medium | GET /products/{id} returns 200 with empty body when product does not exist or id is invalid | When you ask for a product that does not exist (or type letters instead of a product number), the system answers "OK, success" but sends back nothing. It should clearly say "product not found" (or "invalid product number"). Because it pretends everything worked, apps using it show blank pages or crash instead of a helpful message. The same happens for carts and users, and for updating or deleting things that do not exist. | FS-PRODUCTS-005, FS-PRODUCTS-006, FS-PRODUCTS-011, FS-PRODUCTS-013, FS-CARTS-003, FS-CARTS-009, FS-CARTS-010, FS-USERS-004, FS-USERS-011, FS-USERS-012 | draft |
| BUG-003 | Medium | GET /carts/{id} products items do not match the documented Cart schema | When you open a shopping cart, the list of items inside it looks different from what the API documentation promises. The documentation says each item comes with full product details (name, price, picture), but the system only sends a product number and quantity. Developers who follow the documentation will build screens that break; either the system or the documentation needs to be fixed so they match. | FS-CARTS-002 | draft |
| BUG-004 | Medium | POST /products, /carts and /users return 201 when the request body is empty or invalid | The system lets you create products, carts and users with missing or wrong information - an empty form, a price written as text, or an email that is not an email - and says they were created successfully. It should refuse and tell you exactly which detail is missing or wrong. Otherwise broken products, empty carts and unreachable accounts can end up in the store. | FS-PRODUCTS-008, FS-PRODUCTS-014, FS-PRODUCTS-018, FS-CARTS-007, FS-CARTS-011, FS-CARTS-012, FS-USERS-006, FS-USERS-013, FS-USERS-014 | draft |
| BUG-005 | Low | POST /auth/login returns 201 instead of documented 200 on success | When a user logs in successfully, the system replies with a slightly different success code than the documentation says ("created" instead of plain "OK"). Login still works, so users won't notice, but apps that check for the exact documented code may wrongly treat a good login as a failure. | FS-AUTH-001 | draft |

## 6. Assumptions and open questions

- The spec defines no query parameters; ?limit and ?sort (FS-PRODUCTS-002/003) are undocumented but tested because the API supports them.
- Writes (POST/PUT/DELETE) are faked by this API and never persisted, so create-then-read chains cannot be tested.
- Spec has no field-level required/min/max rules: is a negative price valid? (POST accepts price -5.)
- GET /products/categories, /products/category/{name} and /carts/user/{id} exist but are not in the spec - coverage gap.
- Malformed JSON and unknown routes return an HTML error page instead of JSON (observation).
- PATCH /products/{id} works (200) but is not documented.
