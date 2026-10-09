# Test cases — Fake Store API

Environment: public (https://fakestoreapi.com) · Source: docs/openapi.json (OpenAPI 3.1, /docs-data) + https://fakestoreapi.com/docs · Author: QA / Claude · Date: 2026-10-09

## Coverage summary

| Module | Endpoints | Positive | Negative | Total |
|---|---|---|---|---|
| Products | 9 | 12 | 17 | 29 |
| Carts | 7 | 10 | 17 | 27 |
| Users | 6 | 8 | 16 | 24 |
| Auth | 2 | 2 | 9 | 11 |
| Integration | 10 | 10 | 0 | 10 |
| **All** | **34** | **42** | **59** | **101** |

## Products

List, limit/sort, single, categories, create/update/delete, transport security

Endpoints: `GET /products`, `GET /products/{id}`, `GET /products/categories`, `GET /products/category/{name}`, `POST /products`, `PUT /products/{id}`, `PATCH /products/{id}`, `DELETE /products/{id}`, `GET http://.../products/{id}`

### Positive scenarios (12)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-001 | List all products | `GET /products` | Happy path | P0 | - | 200; 20 products; Product schema |
| FS-PRODUCTS-002 | Limit returns that many products | `GET /products` | List | P2 | limit=5 | products 1-5 |
| FS-PRODUCTS-003 | Sort orders products by id | `GET /products` | List | P2 | sort=asc / sort=desc | ids in that order |
| FS-PRODUCTS-005 | List responds within sla | `GET /products` | Performance | P2 | - | response within 2000 ms |
| FS-PRODUCTS-006 | Get single product | `GET /products/{id}` | Happy path | P0 | id=1 | 200; Product schema |
| FS-PRODUCTS-010 | List categories | `GET /products/categories` | Happy path | P0 | - | 200; 4 category names |
| FS-PRODUCTS-011 | Products in category belong to it | `GET /products/category/{name}` | Happy path | P2 | electronics / men's clothing | only products of that category |
| FS-PRODUCTS-013 | Create product | `POST /products` | Happy path | P0 | title, price, description, image, category | 201; new id; fields echoed |
| FS-PRODUCTS-018 | Update product with put | `PUT /products/{id}` | Happy path | P0 | id=1, title + price | 200; id 1, new title |
| FS-PRODUCTS-019 | Update product with patch | `PATCH /products/{id}` | Happy path | P2 | id=1, price 1.25 | 200; price 1.25 |
| FS-PRODUCTS-024 | Delete product | `DELETE /products/{id}` | Happy path | P0 | id=1 | 200; deleted product |
| FS-PRODUCTS-028 | Plain http redirects to https | `GET http://.../products/{id}` | Security | P1 | plain HTTP | 301/308 redirect to HTTPS |

### Negative scenarios (17)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-004 | Invalid list params never break the list | `GET /products` | Validation | P2 | limit=-1 / limit=abc / sort=sideways | no 5xx: 400 or the normal list |
| FS-PRODUCTS-007 | Get nonexistent product returns 4xx | `GET /products/{id}` | Error handling | P1 | id=9999 | 400/404, not an empty 200 |
| FS-PRODUCTS-008 | Get product out of range id returns 4xx | `GET /products/{id}` | Validation | P2 | id=0 / id=-1 | 400/404, not an empty 200 |
| FS-PRODUCTS-009 | Get product non integer id returns 400 | `GET /products/{id}` | Validation | P2 | id=abc / id=1.5 | 400 (spec: id is integer) |
| FS-PRODUCTS-012 | Unknown category returns empty list | `GET /products/category/{name}` | List | P2 | unknown category | 200 [] |
| FS-PRODUCTS-014 | Create product with empty body returns 400 | `POST /products` | Validation | P2 | {} | 400 |
| FS-PRODUCTS-015 | Create product with invalid field returns 400 | `POST /products` | Validation | P2 | price 'abc' / price -10 / image 'not a url' | 400 (spec: number, uri) |
| FS-PRODUCTS-016 | Create product with malformed json returns 400 | `POST /products` | Validation | P2 | body '{bad json' | 400 |
| FS-PRODUCTS-017 | Malformed json error is returned as json | `POST /products` | Contract | P2 | body '{bad json' | error body is JSON, not an HTML page |
| FS-PRODUCTS-020 | Update nonexistent product returns 4xx | `PUT /products/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-PRODUCTS-021 | Update product non integer id returns 400 | `PUT /products/{id}` | Validation | P2 | id=abc | 400 |
| FS-PRODUCTS-022 | Update product with text price returns 400 | `PUT /products/{id}` | Validation | P2 | price 'abc' | 400 |
| FS-PRODUCTS-023 | Id in body does not override url id | `PUT /products/{id}` | Validation | P2 | URL id 1, body id 777 | product 1 updated (body id ignored) or 400 |
| FS-PRODUCTS-025 | Delete nonexistent product returns 4xx | `DELETE /products/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-PRODUCTS-026 | Delete product non integer id returns 400 | `DELETE /products/{id}` | Validation | P2 | id=abc | 400 |
| FS-PRODUCTS-027 | Delete product without login is rejected | `DELETE /products/{id}` | Security | P1 | no token | 401/403 |
| FS-PRODUCTS-029 | Response does not reveal server framework | `GET /products/{id}` | Security | P1 | - | no X-Powered-By header |

## Carts

List, limit/sort, date range, by user, single, create/update/delete

Endpoints: `GET /carts`, `GET /carts/user/{userId}`, `GET /carts/{id}`, `POST /carts`, `PUT /carts/{id}`, `PATCH /carts/{id}`, `DELETE /carts/{id}`

### Positive scenarios (10)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-CARTS-001 | List all carts | `GET /carts` | Happy path | P0 | - | 200; carts with productId/quantity lines |
| FS-CARTS-002 | Limit and sort carts | `GET /carts` | List | P2 | limit=2&sort=desc | 2 carts, ids descending |
| FS-CARTS-003 | Date range returns only carts in range | `GET /carts` | List | P2 | startdate=2020-01-01&enddate=2020-03-01 | only carts dated in range |
| FS-CARTS-006 | Get carts of a user | `GET /carts/user/{userId}` | Happy path | P2 | userId=2 | only carts of user 2 |
| FS-CARTS-009 | Get single cart | `GET /carts/{id}` | Happy path | P0 | id=1 | 200; cart 1 |
| FS-CARTS-010 | Single cart matches spec schema | `GET /carts/{id}` | Contract | P2 | id=1 | matches OpenAPI Cart (products[] are Product) |
| FS-CARTS-013 | Create cart | `POST /carts` | Happy path | P0 | userId 1, date, product 1 x2 | 201; fields echoed |
| FS-CARTS-020 | Update cart with put | `PUT /carts/{id}` | Happy path | P0 | id=1, product 2 x3 | 200; products replaced |
| FS-CARTS-021 | Update cart with patch | `PATCH /carts/{id}` | Happy path | P2 | id=1, product 5 | 200; id 1 |
| FS-CARTS-025 | Delete cart | `DELETE /carts/{id}` | Happy path | P0 | id=1 | 200; deleted cart |

### Negative scenarios (17)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-CARTS-004 | Invalid date format returns 400 | `GET /carts` | Validation | P2 | startdate=notadate | 400 'yyyy-mm-dd' |
| FS-CARTS-005 | Reversed date range returns empty list | `GET /carts` | List | P2 | startdate after enddate | 200 [] or 400 |
| FS-CARTS-007 | Carts of unknown user is empty or 4xx | `GET /carts/user/{userId}` | Error handling | P2 | userId=9999 | 200 [] or 400/404 |
| FS-CARTS-008 | Carts of non integer user returns 400 | `GET /carts/user/{userId}` | Validation | P2 | userId=abc | 400 |
| FS-CARTS-011 | Get nonexistent cart returns 4xx | `GET /carts/{id}` | Error handling | P1 | id=9999 | 400/404, not 200 null |
| FS-CARTS-012 | Get cart non integer id returns 400 | `GET /carts/{id}` | Validation | P2 | id=abc | 400 |
| FS-CARTS-014 | Create cart with empty body returns 400 | `POST /carts` | Validation | P2 | {} | 400 |
| FS-CARTS-015 | Create cart with wrong types returns 400 | `POST /carts` | Validation | P2 | userId 'abc' / products 'x' / date 'notadate' | 400 |
| FS-CARTS-016 | Create cart for unknown user is rejected | `POST /carts` | Validation | P2 | userId 9999 | 400/404 |
| FS-CARTS-017 | Create cart with unknown product is rejected | `POST /carts` | Validation | P2 | productId 99999 | 400/404 |
| FS-CARTS-018 | Create cart with invalid quantity returns 400 | `POST /carts` | Validation | P2 | quantity -2 / 0 | 400 |
| FS-CARTS-019 | Create cart without login is rejected | `POST /carts` | Security | P1 | no token, userId 1 | 401/403 |
| FS-CARTS-022 | Update nonexistent cart returns 4xx | `PUT /carts/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-CARTS-023 | Update cart non integer id returns 400 | `PUT /carts/{id}` | Validation | P2 | id=abc | 400 |
| FS-CARTS-024 | Update cart with negative quantity returns 400 | `PUT /carts/{id}` | Validation | P2 | quantity -5 | 400 |
| FS-CARTS-026 | Delete nonexistent cart returns 4xx | `DELETE /carts/{id}` | Error handling | P2 | id=9999 | 400/404, not 200 null |
| FS-CARTS-027 | Delete cart non integer id returns 400 | `DELETE /carts/{id}` | Validation | P2 | id=abc | 400 |

## Users

List, single, create/update/delete, sensitive data, id integrity

Endpoints: `GET /users`, `GET /users/{id}`, `POST /users`, `PUT /users/{id}`, `PUT, PATCH /users/{id}`, `DELETE /users/{id}`

### Positive scenarios (8)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-USERS-001 | List all users | `GET /users` | Happy path | P0 | - | 200; 10 users; User schema |
| FS-USERS-002 | Limit and sort users | `GET /users` | List | P2 | limit=3&sort=desc | users 10, 9, 8 |
| FS-USERS-004 | Get single user | `GET /users/{id}` | Happy path | P0 | id=1 | 200; User schema |
| FS-USERS-008 | Create user | `POST /users` | Happy path | P0 | username, email, password | 201; numeric id |
| FS-USERS-009 | Create user response returns the user | `POST /users` | Contract | P2 | username, email, password | 201 body is the User (username, email echoed) |
| FS-USERS-015 | Update user email | `PUT /users/{id}` | Happy path | P0 | id=2, email | 200; email changed |
| FS-USERS-016 | Update user response identifies the user | `PUT, PATCH /users/{id}` | Contract | P2 | id=2, username | 200 body is the User incl. id 2 |
| FS-USERS-020 | Delete user | `DELETE /users/{id}` | Happy path | P0 | id=1 | 200; deleted user |

### Negative scenarios (16)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-USERS-003 | User list does not expose passwords | `GET /users` | Security | P1 | no auth | no 'password' field |
| FS-USERS-005 | Get nonexistent user returns 4xx | `GET /users/{id}` | Error handling | P1 | id=9999 | 400/404, not 200 null |
| FS-USERS-006 | Get user non integer id returns 400 | `GET /users/{id}` | Validation | P2 | id=abc | 400 |
| FS-USERS-007 | Single user does not expose password | `GET /users/{id}` | Security | P1 | no auth, id=1 | no 'password' field |
| FS-USERS-010 | New user never gets an existing users id | `POST /users` | Data integrity | P2 | 5 new users | no new user gets an existing user's id (1-10) |
| FS-USERS-011 | Create user with empty body returns 400 | `POST /users` | Validation | P2 | {} | 400 |
| FS-USERS-012 | Create user with invalid email returns 400 | `POST /users` | Validation | P2 | email 'not-an-email' | 400 |
| FS-USERS-013 | Create user without password returns 400 | `POST /users` | Validation | P2 | no password | 400 |
| FS-USERS-014 | Create user with existing username is rejected | `POST /users` | Validation | P2 | username of user 2 | 400/409 duplicate |
| FS-USERS-017 | Update nonexistent user returns 4xx | `PUT /users/{id}` | Error handling | P2 | id=9999 | 400/404 |
| FS-USERS-018 | Update user non integer id returns 400 | `PUT /users/{id}` | Validation | P2 | id=abc | 400 |
| FS-USERS-019 | Update user with invalid email returns 400 | `PUT /users/{id}` | Validation | P2 | email 'bad' | 400 |
| FS-USERS-021 | Delete response does not expose password | `DELETE /users/{id}` | Security | P1 | id=1 | no 'password' in response |
| FS-USERS-022 | Delete nonexistent user returns 4xx | `DELETE /users/{id}` | Error handling | P2 | id=9999 | 400/404, not 200 null |
| FS-USERS-023 | Delete user non integer id returns 400 | `DELETE /users/{id}` | Validation | P2 | id=abc | 400 |
| FS-USERS-024 | Delete user without login is rejected | `DELETE /users/{id}` | Security | P1 | no token | 401/403 |

## Auth

Login, token content, error handling

Endpoints: `POST /auth/login`, `GET /auth/login`

### Positive scenarios (2)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-AUTH-001 | Login with valid credentials | `POST /auth/login` | Happy path | P0 | demo user (env FS_USER / FS_PASSWORD) | 200 + token (spec) |
| FS-AUTH-002 | Token is a jwt for the logged in user | `POST /auth/login` | Contract | P0 | demo user | JWT with user = username, numeric sub |

### Negative scenarios (9)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-AUTH-003 | Token has an expiry | `POST /auth/login` | Security | P1 | demo user | token has an 'exp' (expiry) claim |
| FS-AUTH-004 | Login with wrong password returns 401 | `POST /auth/login` | Auth | P1 | wrong password | 401 |
| FS-AUTH-005 | Login with unknown username returns 401 | `POST /auth/login` | Auth | P2 | unknown username | 401 |
| FS-AUTH-006 | Password is case sensitive | `POST /auth/login` | Auth | P2 | password in upper case | 401 |
| FS-AUTH-007 | Login without required fields returns 400 | `POST /auth/login` | Validation | P2 | {} / username only | 400 |
| FS-AUTH-008 | Login with malicious or wrong type input is rejected | `POST /auth/login` | Security | P1 | ' OR '1'='1 / numbers | 400/401, no token |
| FS-AUTH-009 | Login with non json body returns 400 | `POST /auth/login` | Validation | P2 | text/plain body | 400 |
| FS-AUTH-010 | Login errors are returned as json | `POST /auth/login` | Contract | P2 | wrong password | error body is JSON |
| FS-AUTH-011 | Get on login route is not allowed | `GET /auth/login` | Error handling | P2 | wrong method | 404/405 |

## Integration

Login -> user -> carts; cross-module data consistency

Endpoints: `POST /auth/login -> GET /users/{sub}`, `POST /auth/login -> GET /carts/user/{sub}`, `GET /carts -> GET /products`, `GET /carts -> GET /users`, `GET /carts/user/{id} vs GET /carts`, `GET /products/categories vs GET /products`, `GET /products/category/{name} vs GET /products`, `GET /products/{id} vs GET /products`, `GET /users/{id} vs GET /users`, `GET /carts/{id} -> GET /products`

### Positive scenarios (10)

| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| FS-INTEGRATION-001 | Token subject is the logged in user | `POST /auth/login -> GET /users/{sub}` | Integration | P0 | demo user | token subject is the logged-in user |
| FS-INTEGRATION-002 | Logged in user can see own carts | `POST /auth/login -> GET /carts/user/{sub}` | Integration | P2 | demo user | user's own carts returned |
| FS-INTEGRATION-003 | Every cart product exists | `GET /carts -> GET /products` | Integration | P0 | all carts | every cart product exists |
| FS-INTEGRATION-004 | Every cart owner exists | `GET /carts -> GET /users` | Integration | P0 | all carts | every cart owner exists |
| FS-INTEGRATION-005 | Carts by user match full cart list | `GET /carts/user/{id} vs GET /carts` | Integration | P2 | every owner | same carts |
| FS-INTEGRATION-006 | Category list matches product categories | `GET /products/categories vs GET /products` | Integration | P2 | - | same category set |
| FS-INTEGRATION-007 | Category endpoint matches product list | `GET /products/category/{name} vs GET /products` | Integration | P2 | every category | same products |
| FS-INTEGRATION-008 | Product detail matches list entry | `GET /products/{id} vs GET /products` | Integration | P2 | ids 1, 10, 20 | identical records |
| FS-INTEGRATION-009 | User detail matches list entry | `GET /users/{id} vs GET /users` | Integration | P2 | ids 1, 5, 10 | identical records |
| FS-INTEGRATION-010 | Cart value can be priced from catalogue | `GET /carts/{id} -> GET /products` | Integration | P2 | cart 1 | cart priced from catalogue, total > 0 |

## Assumptions and open questions

- Spec documents 200 + 400 'Bad request' for every endpoint; 404 is also accepted for unknown ids, an empty 200 is not.
- Spec defines no required fields; validation expectations come from field types (integer, number, uri) and common sense (no empty records, quantity >= 1).
- limit, sort, startdate/enddate, /products/categories, /products/category/{name}, /carts/user/{id} and PATCH are documented on the website, not in the spec.
- Spec defines no authentication; write-without-login and password exposure are reported as security issues (bugs even if the spec is silent).
- Writes are not persisted, so create -> read lifecycles cannot be verified; integration flows use stored data.
