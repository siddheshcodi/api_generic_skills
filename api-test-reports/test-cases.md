# Test cases — Fake Store API (demo)

Environment: public (https://fakestoreapi.com) · Source: docs/openapi.json (OpenAPI 3.1 from /docs-data) · Author: Claude (api-testing skill) · Date: 2026-10-09

## Coverage summary

| Module | Endpoints | Positive | Negative | Total |
|---|---|---|---|---|
| Products | 5 | 7 | 11 | 18 |
| Carts | 5 | 5 | 7 | 12 |
| Users | 6 | 5 | 9 | 14 |
| Auth | 1 | 2 | 6 | 8 |
| Integration | 7 | 7 | 0 | 7 |
| **All** | **24** | **26** | **33** | **59** |

## Products

Product catalogue: list, filter, read, create, update, delete.

Endpoints: `GET /products`, `GET /products/{id}`, `POST /products`, `PUT /products/{id}`, `DELETE /products/{id}`

### Positive scenarios (7)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-001 | List all products | `GET /products` | Happy path / contract | P0 | no params | 200, JSON list, every item matches Product schema |
| FS-PRODUCTS-002 | Limit the number of products | `GET /products` | List / pagination | P2 | ?limit=5 | 200 with exactly 5 items |
| FS-PRODUCTS-003 | Sort products descending | `GET /products` | List / sort | P2 | ?sort=desc | 200, ids in descending order |
| FS-PRODUCTS-004 | Get a single product | `GET /products/{id}` | Happy path / contract | P0 | id=1 | 200, Product with id 1 |
| FS-PRODUCTS-007 | Create a product with valid data | `POST /products` | Happy path | P0 | title, price, description, category, image | 201, id returned, fields echoed |
| FS-PRODUCTS-010 | Update a product | `PUT /products/{id}` | Happy path | P1 | id=1, valid body | 200, title updated |
| FS-PRODUCTS-012 | Delete a product | `DELETE /products/{id}` | Happy path | P1 | id=1 | 200 |

### Negative scenarios (11)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-005 | Get a product that does not exist | `GET /products/{id}` | Error handling | P1 | id=9999 | 400/404, not an empty 200 |
| FS-PRODUCTS-006 | Get a product with a non-numeric id | `GET /products/{id}` | Validation | P2 | id=abc | 400 (spec: id is integer) |
| FS-PRODUCTS-008 | Create a product with an empty body | `POST /products` | Validation | P1 | {} | 400 (request body is required) |
| FS-PRODUCTS-009 | Create a product with malformed JSON | `POST /products` | Validation | P2 | body: not json | 400, never 5xx |
| FS-PRODUCTS-011 | Update a product that does not exist | `PUT /products/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-PRODUCTS-013 | Delete a product that does not exist | `DELETE /products/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-PRODUCTS-014 | Create a product with text as price | `POST /products` | Validation / data type | P2 | price: "abc" | 400 (spec: price is a number) |
| FS-PRODUCTS-015 | Create a product with a 10,000-character title | `POST /products` | Boundary | P3 | "title": "a" x 10000 | no 5xx (spec sets no max length; 400/413 preferred) |
| FS-PRODUCTS-016 | Update a product with a non-numeric id | `PUT /products/{id}` | Validation | P2 | id=abc | 400 |
| FS-PRODUCTS-017 | Delete a product with a non-numeric id | `DELETE /products/{id}` | Validation | P2 | id=abc | 400 |
| FS-PRODUCTS-018 | Create a product with a non-JSON body | `POST /products` | Validation / content type | P2 | Content-Type text/plain, body title=x | 400/415 |

## Carts

Shopping carts of users: list, read, create, update, delete.

Endpoints: `GET /carts`, `GET /carts/{id}`, `POST /carts`, `PUT /carts/{id}`, `DELETE /carts/{id}`

### Positive scenarios (5)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-CARTS-001 | List all carts | `GET /carts` | Happy path | P0 | no params | 200, non-empty list |
| FS-CARTS-002 | Get a single cart matching the documented schema | `GET /carts/{id}` | Contract | P1 | id=1 | 200, products[] items are Product objects (per spec) |
| FS-CARTS-004 | Create a cart | `POST /carts` | Happy path | P1 | userId=1, products=[...] | 201 with id |
| FS-CARTS-005 | Update a cart | `PUT /carts/{id}` | Happy path | P1 | id=1, new products | 200, products updated |
| FS-CARTS-006 | Delete a cart | `DELETE /carts/{id}` | Happy path | P1 | id=1 | 200 |

### Negative scenarios (7)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-CARTS-003 | Get a cart that does not exist | `GET /carts/{id}` | Error handling | P2 | id=9999 | 400/404, not 200 null |
| FS-CARTS-007 | Create a cart with an empty body | `POST /carts` | Validation | P1 | {} | 400 (no userId / products) |
| FS-CARTS-008 | Get a cart with a non-numeric id | `GET /carts/{id}` | Validation | P2 | id=abc | 400 |
| FS-CARTS-009 | Update a cart that does not exist | `PUT /carts/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-CARTS-010 | Delete a cart that does not exist | `DELETE /carts/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-CARTS-011 | Create a cart with text as userId | `POST /carts` | Validation / data type | P2 | "userId": "abc" | 400 (spec: integer) |
| FS-CARTS-012 | Create a cart where products is not a list | `POST /carts` | Validation / data type | P2 | "products": "x" | 400 (spec: array) |

## Users

Customer accounts: list, read, create, update, delete. Includes sensitive-data checks.

Endpoints: `GET /users`, `GET /users/{id}`, `POST /users`, `PUT /users/{id}`, `DELETE /users/{id}`, `GET, DELETE /users/{id}`

### Positive scenarios (5)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-USERS-001 | List all users | `GET /users` | Happy path / contract | P0 | no params | 200, every item matches User schema |
| FS-USERS-002 | Get a single user | `GET /users/{id}` | Happy path / contract | P0 | id=1 | 200, User object |
| FS-USERS-005 | Create a user with valid data | `POST /users` | Happy path | P1 | username, email, password | 201 with id |
| FS-USERS-007 | Update a user | `PUT /users/{id}` | Happy path | P1 | id=1, new username | 200, username updated |
| FS-USERS-008 | Delete a user | `DELETE /users/{id}` | Happy path | P1 | id=1 | 200 |

### Negative scenarios (9)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-USERS-003 | User list must not expose passwords | `GET /users` | Security - sensitive data | P1 | no auth | no 'password' field in any user |
| FS-USERS-004 | Get a user that does not exist | `GET /users/{id}` | Error handling | P2 | id=9999 | 400/404, not 200 null |
| FS-USERS-006 | Create a user with an invalid email | `POST /users` | Validation / format | P1 | email: not-an-email | 400 |
| FS-USERS-009 | Single-user responses must not expose password | `GET, DELETE /users/{id}` | Security - sensitive data | P1 | GET and DELETE /users/1 | no 'password' field in the response |
| FS-USERS-010 | Get a user with a non-numeric id | `GET /users/{id}` | Validation | P2 | id=abc | 400 |
| FS-USERS-011 | Update a user that does not exist | `PUT /users/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-USERS-012 | Delete a user that does not exist | `DELETE /users/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-USERS-013 | Create a user with an empty body | `POST /users` | Validation | P1 | {} | 400 |
| FS-USERS-014 | Create a user without a password | `POST /users` | Validation | P1 | username + email only | 400 |

## Auth

Login that returns a token.

Endpoints: `POST /auth/login`

### Positive scenarios (2)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-AUTH-001 | Login with valid credentials | `POST /auth/login` | Happy path / contract | P0 | demo user (env FS_USER / FS_PASSWORD) | 200 + token (per spec) |
| FS-AUTH-008 | Login token is a well-formed JWT | `POST /auth/login` | Contract | P1 | demo user | token has 3 non-empty parts (header.payload.signature) |

### Negative scenarios (6)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-AUTH-002 | Login with a wrong password | `POST /auth/login` | Auth | P0 | valid user, wrong password | 401 |
| FS-AUTH-003 | Login with an empty body | `POST /auth/login` | Validation | P1 | {} | 400 |
| FS-AUTH-004 | Login with SQL-injection-like input | `POST /auth/login` | Security | P2 | ' OR '1'='1 | 400/401, no 5xx, no token |
| FS-AUTH-005 | Login with an unknown username | `POST /auth/login` | Auth | P1 | qa_auto_nobody | 401 |
| FS-AUTH-006 | Login without a password | `POST /auth/login` | Validation | P1 | username only | 400 |
| FS-AUTH-007 | Login with numbers instead of text | `POST /auth/login` | Validation / data type | P2 | username 123, password 456 | 400/401, no token |

## Integration

Cross-module flows and data consistency between Auth, Users, Carts and Products (read-only, because this API does not save writes).

Endpoints: `POST /auth/login → GET /users → GET /carts`, `GET /carts → GET /products`, `GET /carts → GET /users`, `GET /products → GET /products/{id}`, `POST /auth/login → GET /users`, `GET /users → GET /users/{id}`, `GET /carts → GET /carts/{id}`

### Positive scenarios (7)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-INTEG-001 | Logged-in user has a profile and their own carts | `POST /auth/login → GET /users → GET /carts` | Integration flow | P1 | demo user login | login gives token; user found in /users; at least one cart with that userId |
| FS-INTEG-002 | Every product in any cart exists in the catalogue | `GET /carts → GET /products` | Integration flow | P1 | all carts, all products | every cart productId is a real product id |
| FS-INTEG-003 | Every cart belongs to an existing user | `GET /carts → GET /users` | Integration flow | P1 | all carts, all users | every cart userId is a real user id |
| FS-INTEG-004 | Product list and product detail return the same data | `GET /products → GET /products/{id}` | Integration flow | P1 | first 5 products | detail equals the list item for each product |
| FS-INTEG-005 | Login token identifies the same user | `POST /auth/login → GET /users` | Integration flow | P1 | demo user login | token 'sub' claim equals that user's id in /users |
| FS-INTEG-006 | User list and user detail return the same data | `GET /users → GET /users/{id}` | Integration flow | P2 | first 5 users | detail equals the list item for each user |
| FS-INTEG-007 | Cart list and cart detail return the same data | `GET /carts → GET /carts/{id}` | Integration flow | P2 | first 5 carts | detail equals the list item for each cart |

## Assumptions and open questions

- The spec defines no query parameters; ?limit and ?sort (FS-PRODUCTS-002/003) are undocumented but tested because the API supports them.
- Writes (POST/PUT/DELETE) are faked by this API and never persisted, so create-then-read chains cannot be tested.
- Spec has no field-level required/min/max rules: is a negative price valid? (POST accepts price -5.)
- GET /products/categories, /products/category/{name} and /carts/user/{id} exist but are not in the spec - coverage gap.
- Malformed JSON and unknown routes return an HTML error page instead of JSON (observation).
- PATCH /products/{id} works (200) but is not documented.
