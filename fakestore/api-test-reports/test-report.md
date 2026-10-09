# API Test Report — Fake Store API

Environment: public (https://fakestoreapi.com) · Source: docs/openapi.json (OpenAPI 3.1, /docs-data) + https://fakestoreapi.com/docs · Date: 2026-10-09

## 1. Overall result

| Total | Passed | Failed | Errors | Skipped | Not run | Pass rate |
|---|---|---|---|---|---|---|
| 101 | 61 | 40 | 0 | 0 | 0 | 60.4% |

| Scenario type | Total | Passed | Failed | Pass rate |
|---|---|---|---|---|
| Positive | 42 | 38 | 4 | 90.5% |
| Negative | 59 | 23 | 36 | 39.0% |

Bugs: Critical 1 · High 2 · Medium 6 · Low 3 (total 12)

## 2. Module summary

| Module | Endpoints | Positive | Negative | Total | Passed | Failed | Pass rate | Bugs |
|---|---|---|---|---|---|---|---|---|
| Products | 9 | 12 | 17 | 29 | 18 | 11 | 62.1% | BUG-002, BUG-005, BUG-006, BUG-010, BUG-012 |
| Carts | 7 | 10 | 17 | 27 | 16 | 11 | 59.3% | BUG-002, BUG-005, BUG-006, BUG-008 |
| Users | 6 | 8 | 16 | 24 | 9 | 15 | 37.5% | BUG-001, BUG-002, BUG-004, BUG-005, BUG-006, BUG-007, BUG-009 |
| Auth | 2 | 2 | 9 | 11 | 8 | 3 | 72.7% | BUG-003, BUG-010, BUG-011 |
| Integration | 10 | 10 | 0 | 10 | 10 | 0 | 100.0% | – |

## 3. Module details

### Products — 18/29 passed

List, limit/sort, single, categories, create/update/delete, transport security

#### Positive scenarios (12)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-001 | List all products | `GET /products` | 200; 20 products; Product schema | ✅ Pass |  |  |
| FS-PRODUCTS-002 | Limit returns that many products | `GET /products` | products 1-5 | ✅ Pass |  |  |
| FS-PRODUCTS-003 | Sort orders products by id | `GET /products` | ids in that order | ✅ Pass |  |  |
| FS-PRODUCTS-005 | List responds within sla | `GET /products` | response within 2000 ms | ✅ Pass |  |  |
| FS-PRODUCTS-006 | Get single product | `GET /products/{id}` | 200; Product schema | ✅ Pass |  |  |
| FS-PRODUCTS-010 | List categories | `GET /products/categories` | 200; 4 category names | ✅ Pass |  |  |
| FS-PRODUCTS-011 | Products in category belong to it | `GET /products/category/{name}` | only products of that category | ✅ Pass |  |  |
| FS-PRODUCTS-013 | Create product | `POST /products` | 201; new id; fields echoed | ✅ Pass |  |  |
| FS-PRODUCTS-018 | Update product with put | `PUT /products/{id}` | 200; id 1, new title | ✅ Pass |  |  |
| FS-PRODUCTS-019 | Update product with patch | `PATCH /products/{id}` | 200; price 1.25 | ✅ Pass |  |  |
| FS-PRODUCTS-024 | Delete product | `DELETE /products/{id}` | 200; deleted product | ✅ Pass |  |  |
| FS-PRODUCTS-028 | Plain http redirects to https | `GET http://.../products/{id}` | 301/308 redirect to HTTPS | ✅ Pass |  |  |

#### Negative scenarios (17)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-PRODUCTS-004 | Invalid list params never break the list | `GET /products` | no 5xx: 400 or the normal list | ✅ Pass |  |  |
| FS-PRODUCTS-007 | Get nonexistent product returns 4xx | `GET /products/{id}` | 400/404, not an empty 200 | ❌ Fail | expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/products/9999 -> 200: '' | BUG-005 |
| FS-PRODUCTS-008 | Get product out of range id returns 4xx | `GET /products/{id}` | 400/404, not an empty 200 | ❌ Fail | expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/products/0 -> 200: '' | BUG-005 |
| FS-PRODUCTS-009 | Get product non integer id returns 400 | `GET /products/{id}` | 400 (spec: id is integer) | ❌ Fail | spec: id is an integer; expected 400 for 'abc', got GET https://fakestoreapi.com/products/abc -> 200: '' | BUG-005 |
| FS-PRODUCTS-012 | Unknown category returns empty list | `GET /products/category/{name}` | 200 [] | ✅ Pass |  |  |
| FS-PRODUCTS-014 | Create product with empty body returns 400 | `POST /products` | 400 | ❌ Fail | a product with no data should be rejected, got POST https://fakestoreapi.com/products -> 201: '{"id":21}' | BUG-006 |
| FS-PRODUCTS-015 | Create product with invalid field returns 400 | `POST /products` | 400 (spec: number, uri) | ❌ Fail | price='abc' should be rejected, got POST https://fakestoreapi.com/products -> 201: '{"id":21,"title":"qa_auto product","price":"abc","description":"created by API test","image":"https://i.pravatar.cc","category":"electro | BUG-006 |
| FS-PRODUCTS-016 | Create product with malformed json returns 400 | `POST /products` | 400 | ✅ Pass |  |  |
| FS-PRODUCTS-017 | Malformed json error is returned as json | `POST /products` | error body is JSON, not an HTML page | ❌ Fail | error body is 'text/html; charset=utf-8', not JSON: '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>Error</tit' | BUG-010 |
| FS-PRODUCTS-020 | Update nonexistent product returns 4xx | `PUT /products/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown/invalid id, got PUT https://fakestoreapi.com/products/9999 -> 200: '{"id":9999,"title":"x"}' | BUG-005 |
| FS-PRODUCTS-021 | Update product non integer id returns 400 | `PUT /products/{id}` | 400 | ✅ Pass |  |  |
| FS-PRODUCTS-022 | Update product with text price returns 400 | `PUT /products/{id}` | 400 | ❌ Fail | price 'abc' should be rejected, got PUT https://fakestoreapi.com/products/1 -> 200: '{"id":1,"price":"abc"}' | BUG-006 |
| FS-PRODUCTS-023 | Id in body does not override url id | `PUT /products/{id}` | product 1 updated (body id ignored) or 400 | ✅ Pass |  |  |
| FS-PRODUCTS-025 | Delete nonexistent product returns 4xx | `DELETE /products/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown/invalid id, got DELETE https://fakestoreapi.com/products/9999 -> 200: '' | BUG-005 |
| FS-PRODUCTS-026 | Delete product non integer id returns 400 | `DELETE /products/{id}` | 400 | ✅ Pass |  |  |
| FS-PRODUCTS-027 | Delete product without login is rejected | `DELETE /products/{id}` | 401/403 | ❌ Fail | anyone can delete a product without logging in: DELETE https://fakestoreapi.com/products/1 -> 200: '{"id":1,"title":"Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops","price":109.95,"description":"Your perfect pack  | BUG-002 |
| FS-PRODUCTS-029 | Response does not reveal server framework | `GET /products/{id}` | no X-Powered-By header | ❌ Fail | X-Powered-By: Express | BUG-012 |

### Carts — 16/27 passed

List, limit/sort, date range, by user, single, create/update/delete

#### Positive scenarios (10)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-CARTS-001 | List all carts | `GET /carts` | 200; carts with productId/quantity lines | ✅ Pass |  |  |
| FS-CARTS-002 | Limit and sort carts | `GET /carts` | 2 carts, ids descending | ✅ Pass |  |  |
| FS-CARTS-003 | Date range returns only carts in range | `GET /carts` | only carts dated in range | ✅ Pass |  |  |
| FS-CARTS-006 | Get carts of a user | `GET /carts/user/{userId}` | only carts of user 2 | ✅ Pass |  |  |
| FS-CARTS-009 | Get single cart | `GET /carts/{id}` | 200; cart 1 | ✅ Pass |  |  |
| FS-CARTS-010 | Single cart matches spec schema | `GET /carts/{id}` | matches OpenAPI Cart (products[] are Product) | ❌ Fail | jsonschema.exceptions.ValidationError: 'id' is a required property | BUG-008 |
| FS-CARTS-013 | Create cart | `POST /carts` | 201; fields echoed | ✅ Pass |  |  |
| FS-CARTS-020 | Update cart with put | `PUT /carts/{id}` | 200; products replaced | ✅ Pass |  |  |
| FS-CARTS-021 | Update cart with patch | `PATCH /carts/{id}` | 200; id 1 | ✅ Pass |  |  |
| FS-CARTS-025 | Delete cart | `DELETE /carts/{id}` | 200; deleted cart | ✅ Pass |  |  |

#### Negative scenarios (17)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-CARTS-004 | Invalid date format returns 400 | `GET /carts` | 400 'yyyy-mm-dd' | ✅ Pass |  |  |
| FS-CARTS-005 | Reversed date range returns empty list | `GET /carts` | 200 [] or 400 | ✅ Pass |  |  |
| FS-CARTS-007 | Carts of unknown user is empty or 4xx | `GET /carts/user/{userId}` | 200 [] or 400/404 | ✅ Pass |  |  |
| FS-CARTS-008 | Carts of non integer user returns 400 | `GET /carts/user/{userId}` | 400 | ✅ Pass |  |  |
| FS-CARTS-011 | Get nonexistent cart returns 4xx | `GET /carts/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/carts/9999 -> 200: 'null' | BUG-005 |
| FS-CARTS-012 | Get cart non integer id returns 400 | `GET /carts/{id}` | 400 | ✅ Pass |  |  |
| FS-CARTS-014 | Create cart with empty body returns 400 | `POST /carts` | 400 | ❌ Fail | a cart with no user or products should be rejected, got POST https://fakestoreapi.com/carts -> 201: '{"id":11}' | BUG-006 |
| FS-CARTS-015 | Create cart with wrong types returns 400 | `POST /carts` | 400 | ❌ Fail | {'userId': 'abc'} should be rejected, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":"abc","date":"2026-10-09","products":[{"productId":1,"quantity":2}]}' | BUG-006 |
| FS-CARTS-016 | Create cart for unknown user is rejected | `POST /carts` | 400/404 | ❌ Fail | user 9999 does not exist, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":9999,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}' | BUG-006 |
| FS-CARTS-017 | Create cart with unknown product is rejected | `POST /carts` | 400/404 | ❌ Fail | product 99999 does not exist, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":99999,"quantity":1}]}' | BUG-006 |
| FS-CARTS-018 | Create cart with invalid quantity returns 400 | `POST /carts` | 400 | ❌ Fail | quantity -2 should be rejected, got POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":-2}]}' | BUG-006 |
| FS-CARTS-019 | Create cart without login is rejected | `POST /carts` | 401/403 | ❌ Fail | anyone can create a cart for user 1 without logging in: POST https://fakestoreapi.com/carts -> 201: '{"id":11,"userId":1,"date":"2026-10-09","products":[{"productId":1,"quantity":2}]}' | BUG-002 |
| FS-CARTS-022 | Update nonexistent cart returns 4xx | `PUT /carts/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown/invalid id, got PUT https://fakestoreapi.com/carts/9999 -> 200: '{"id":9999,"userId":1,"products":[{"productId":1,"quantity":1}]}' | BUG-005 |
| FS-CARTS-023 | Update cart non integer id returns 400 | `PUT /carts/{id}` | 400 | ✅ Pass |  |  |
| FS-CARTS-024 | Update cart with negative quantity returns 400 | `PUT /carts/{id}` | 400 | ❌ Fail | quantity -5 should be rejected, got PUT https://fakestoreapi.com/carts/1 -> 200: '{"id":1,"userId":1,"products":[{"productId":1,"quantity":-5}]}' | BUG-006 |
| FS-CARTS-026 | Delete nonexistent cart returns 4xx | `DELETE /carts/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown/invalid id, got DELETE https://fakestoreapi.com/carts/9999 -> 200: 'null' | BUG-005 |
| FS-CARTS-027 | Delete cart non integer id returns 400 | `DELETE /carts/{id}` | 400 | ✅ Pass |  |  |

### Users — 9/24 passed

List, single, create/update/delete, sensitive data, id integrity

#### Positive scenarios (8)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-USERS-001 | List all users | `GET /users` | 200; 10 users; User schema | ✅ Pass |  |  |
| FS-USERS-002 | Limit and sort users | `GET /users` | users 10, 9, 8 | ✅ Pass |  |  |
| FS-USERS-004 | Get single user | `GET /users/{id}` | 200; User schema | ✅ Pass |  |  |
| FS-USERS-008 | Create user | `POST /users` | 201; numeric id | ✅ Pass |  |  |
| FS-USERS-009 | Create user response returns the user | `POST /users` | 201 body is the User (username, email echoed) | ❌ Fail | spec: 201 returns the User; response is {'id': 11} (missing ['username', 'email']) | BUG-009 |
| FS-USERS-015 | Update user email | `PUT /users/{id}` | 200; email changed | ✅ Pass |  |  |
| FS-USERS-016 | Update user response identifies the user | `PUT, PATCH /users/{id}` | 200 body is the User incl. id 2 | ❌ Fail | spec: 200 returns the User; PUT response has no id: {'username': 'qa_auto_user'} | BUG-009 |
| FS-USERS-020 | Delete user | `DELETE /users/{id}` | 200; deleted user | ✅ Pass |  |  |

#### Negative scenarios (16)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-USERS-003 | User list does not expose passwords | `GET /users` | no 'password' field | ❌ Fail | GET /users (no login needed) returns 'password' for user ids [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] | BUG-001 |
| FS-USERS-005 | Get nonexistent user returns 4xx | `GET /users/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown/invalid id, got GET https://fakestoreapi.com/users/9999 -> 200: 'null' | BUG-005 |
| FS-USERS-006 | Get user non integer id returns 400 | `GET /users/{id}` | 400 | ✅ Pass |  |  |
| FS-USERS-007 | Single user does not expose password | `GET /users/{id}` | no 'password' field | ❌ Fail | GET /users/1 (no login needed) returns the user's password | BUG-001 |
| FS-USERS-010 | New user never gets an existing users id | `POST /users` | no new user gets an existing user's id (1-10) | ❌ Fail | 5 new users got ids [1, 11, 11, 11, 1]; 2 reuse an existing user's id | BUG-004 |
| FS-USERS-011 | Create user with empty body returns 400 | `POST /users` | 400 | ❌ Fail | a user with no data should be rejected, got POST https://fakestoreapi.com/users -> 201: '{"id":1}' | BUG-006 |
| FS-USERS-012 | Create user with invalid email returns 400 | `POST /users` | 400 | ❌ Fail | email 'not-an-email' should be rejected, got POST https://fakestoreapi.com/users -> 201: '{"id":11}' | BUG-006 |
| FS-USERS-013 | Create user without password returns 400 | `POST /users` | 400 | ❌ Fail | a user without password should be rejected, got POST https://fakestoreapi.com/users -> 201: '{"id":1}' | BUG-006 |
| FS-USERS-014 | Create user with existing username is rejected | `POST /users` | 400/409 duplicate | ❌ Fail | username 'mor_2314' already exists, got POST https://fakestoreapi.com/users -> 201: '{"id":11}' | BUG-007 |
| FS-USERS-017 | Update nonexistent user returns 4xx | `PUT /users/{id}` | 400/404 | ❌ Fail | expected 400/404 for unknown/invalid id, got PUT https://fakestoreapi.com/users/9999 -> 200: '{"email":"qa_auto@example.com"}' | BUG-005 |
| FS-USERS-018 | Update user non integer id returns 400 | `PUT /users/{id}` | 400 | ✅ Pass |  |  |
| FS-USERS-019 | Update user with invalid email returns 400 | `PUT /users/{id}` | 400 | ❌ Fail | email 'bad' should be rejected, got PUT https://fakestoreapi.com/users/2 -> 200: '{"email":"bad"}' | BUG-006 |
| FS-USERS-021 | Delete response does not expose password | `DELETE /users/{id}` | no 'password' in response | ❌ Fail | DELETE /users/1 response contains the password | BUG-001 |
| FS-USERS-022 | Delete nonexistent user returns 4xx | `DELETE /users/{id}` | 400/404, not 200 null | ❌ Fail | expected 400/404 for unknown/invalid id, got DELETE https://fakestoreapi.com/users/9999 -> 200: 'null' | BUG-005 |
| FS-USERS-023 | Delete user non integer id returns 400 | `DELETE /users/{id}` | 400 | ✅ Pass |  |  |
| FS-USERS-024 | Delete user without login is rejected | `DELETE /users/{id}` | 401/403 | ❌ Fail | anyone can delete a user account without logging in: DELETE https://fakestoreapi.com/users/1 -> 200: '{"address":{"geolocation":{"lat":"-37.3159","long":"81.1496"},"city":"kilcoole","street":"new road","number":7682,"zip | BUG-002 |

### Auth — 8/11 passed

Login, token content, error handling

#### Positive scenarios (2)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-AUTH-001 | Login with valid credentials | `POST /auth/login` | 200 + token (spec) | ❌ Fail | spec documents 200 LoginResponse, got 201 | BUG-011 |
| FS-AUTH-002 | Token is a jwt for the logged in user | `POST /auth/login` | JWT with user = username, numeric sub | ✅ Pass |  |  |

#### Negative scenarios (9)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-AUTH-003 | Token has an expiry | `POST /auth/login` | token has an 'exp' (expiry) claim | ❌ Fail | token has no 'exp' claim and never expires: claims ['iat', 'sub', 'user'] | BUG-003 |
| FS-AUTH-004 | Login with wrong password returns 401 | `POST /auth/login` | 401 | ✅ Pass |  |  |
| FS-AUTH-005 | Login with unknown username returns 401 | `POST /auth/login` | 401 | ✅ Pass |  |  |
| FS-AUTH-006 | Password is case sensitive | `POST /auth/login` | 401 | ✅ Pass |  |  |
| FS-AUTH-007 | Login without required fields returns 400 | `POST /auth/login` | 400 | ✅ Pass |  |  |
| FS-AUTH-008 | Login with malicious or wrong type input is rejected | `POST /auth/login` | 400/401, no token | ✅ Pass |  |  |
| FS-AUTH-009 | Login with non json body returns 400 | `POST /auth/login` | 400 | ✅ Pass |  |  |
| FS-AUTH-010 | Login errors are returned as json | `POST /auth/login` | error body is JSON | ❌ Fail | error body is 'text/html; charset=utf-8', not JSON: 'username or password is incorrect' | BUG-010 |
| FS-AUTH-011 | Get on login route is not allowed | `GET /auth/login` | 404/405 | ✅ Pass |  |  |

### Integration — 10/10 passed

Login -> user -> carts; cross-module data consistency

#### Positive scenarios (10)

| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |
|---|---|---|---|---|---|---|
| FS-INTEGRATION-001 | Token subject is the logged in user | `POST /auth/login -> GET /users/{sub}` | token subject is the logged-in user | ✅ Pass |  |  |
| FS-INTEGRATION-002 | Logged in user can see own carts | `POST /auth/login -> GET /carts/user/{sub}` | user's own carts returned | ✅ Pass |  |  |
| FS-INTEGRATION-003 | Every cart product exists | `GET /carts -> GET /products` | every cart product exists | ✅ Pass |  |  |
| FS-INTEGRATION-004 | Every cart owner exists | `GET /carts -> GET /users` | every cart owner exists | ✅ Pass |  |  |
| FS-INTEGRATION-005 | Carts by user match full cart list | `GET /carts/user/{id} vs GET /carts` | same carts | ✅ Pass |  |  |
| FS-INTEGRATION-006 | Category list matches product categories | `GET /products/categories vs GET /products` | same category set | ✅ Pass |  |  |
| FS-INTEGRATION-007 | Category endpoint matches product list | `GET /products/category/{name} vs GET /products` | same products | ✅ Pass |  |  |
| FS-INTEGRATION-008 | Product detail matches list entry | `GET /products/{id} vs GET /products` | identical records | ✅ Pass |  |  |
| FS-INTEGRATION-009 | User detail matches list entry | `GET /users/{id} vs GET /users` | identical records | ✅ Pass |  |  |
| FS-INTEGRATION-010 | Cart value can be priced from catalogue | `GET /carts/{id} -> GET /products` | cart priced from catalogue, total > 0 | ✅ Pass |  |  |

## 4. Bugs found

| Bug | Severity | Title | In simple words | Failed tests | Status |
|---|---|---|---|---|---|
| BUG-001 | Critical | GET /users, GET /users/{id} and DELETE /users/{id} return every user's password in plain text | Anyone on the internet, without logging in, can open the user list and read every customer's password in plain text - and those passwords really work to log in. Passwords should never be sent back by the system. With them, a stranger can take over any customer account. | FS-USERS-003, FS-USERS-007, FS-USERS-021 | draft |
| BUG-002 | High | Products, carts and users can be created, changed and deleted without logging in | Anyone, without logging in, can delete products, delete customer accounts, or create shopping carts in another customer's name. Changing data should only be allowed for logged-in people who own the data or are administrators. Right now any visitor or script could wipe or tamper with the store. | FS-PRODUCTS-027, FS-CARTS-019, FS-USERS-024 | draft |
| BUG-003 | High | POST /auth/login issues tokens that never expire | The login key the system hands out after signing in never runs out. If someone steals it (from a shared computer, a log file or a browser), they can use it forever. Login keys should expire after a set time, for example one hour. | FS-AUTH-003 | draft |
| BUG-004 | Medium | POST /users gives a new user the id of an existing user (id 1) in about 40% of calls | When a new customer signs up, the system often gives them the same customer number as an existing customer (number 1). Two people with the same number means one could see or change the other's orders and data. Every new account must get its own unique number. | FS-USERS-010 | draft |
| BUG-005 | Medium | Unknown or invalid ids return 200 with an empty, null or made-up record instead of 400/404 | When you ask for, change or delete a product, cart or user that doesn't exist (or use letters instead of a number), the system answers 'OK, success' and sends back nothing - or even pretends to update item 9999. It should clearly say 'not found' or 'invalid number'. Apps relying on it show blank pages or think a change worked when it didn't. | FS-PRODUCTS-007, FS-PRODUCTS-008, FS-PRODUCTS-009, FS-PRODUCTS-020, FS-PRODUCTS-025, FS-CARTS-011, FS-CARTS-022, FS-CARTS-026, FS-USERS-005, FS-USERS-017, FS-USERS-022 | draft |
| BUG-006 | Medium | Create and update accept empty and invalid data for products, carts and users | The system creates products, carts and users even when the form is empty or clearly wrong - a price written as text or below zero, a picture link that isn't a link, a cart for a customer or product that doesn't exist, a negative or zero quantity, an email that isn't an email, an account with no password - and says 'created successfully'. It should refuse and say which detail is wrong. | FS-PRODUCTS-014, FS-PRODUCTS-015, FS-PRODUCTS-022, FS-CARTS-014, FS-CARTS-015, FS-CARTS-016, FS-CARTS-017, FS-CARTS-018, FS-CARTS-024, FS-USERS-011, FS-USERS-012, FS-USERS-013, FS-USERS-019 | draft |
| BUG-007 | Medium | POST /users accepts a username that already exists | A new account can be created with exactly the same username as an existing customer. Usernames are used to log in, so two accounts with the same name means the wrong person could end up logged in. The system should say 'username already taken'. | FS-USERS-014 | draft |
| BUG-008 | Medium | GET /carts/{id} products do not match the documented Cart schema | The items inside a cart look different from what the API documentation promises. The documentation says each item is a full product (name, price, picture), but the system only sends a product number and a quantity. Developers who follow the documentation build screens that break. | FS-CARTS-010 | draft |
| BUG-009 | Medium | POST, PUT and PATCH /users do not return the user record | After creating or changing a customer account, the system's reply doesn't contain the account: a new account comes back with only a number, and an update comes back without the account number at all. Apps can't confirm what was saved or which account was changed. The reply should contain the full account (without the password). | FS-USERS-009, FS-USERS-016 | draft |
| BUG-010 | Low | Error responses are plain text or HTML pages instead of JSON | When something goes wrong at login (wrong password, missing fields) or the request is badly formed, the system answers with plain text or a web page instead of the structured format it uses everywhere else. Apps can't read these errors reliably and may crash or show raw HTML to the user. | FS-AUTH-010, FS-PRODUCTS-017 | draft |
| BUG-011 | Low | POST /auth/login returns 201 instead of the documented 200 | A successful login answers with a slightly different success code ('created') than the documentation says ('OK'). Login still works, but apps that check for the exact documented code may treat a good login as a failure. | FS-AUTH-001 | draft |
| BUG-012 | Low | Responses reveal the server framework (X-Powered-By: Express) | Every reply tells the world which software the server runs on. This doesn't break anything, but it helps attackers pick known weaknesses for that software. The header should be switched off. | FS-PRODUCTS-029 | draft |

## 6. Assumptions and open questions

- Spec documents 200 + 400 'Bad request' for every endpoint; 404 is also accepted for unknown ids, an empty 200 is not.
- Spec defines no required fields; validation expectations come from field types (integer, number, uri) and common sense (no empty records, quantity >= 1).
- limit, sort, startdate/enddate, /products/categories, /products/category/{name}, /carts/user/{id} and PATCH are documented on the website, not in the spec.
- Spec defines no authentication; write-without-login and password exposure are reported as security issues (bugs even if the spec is silent).
- Writes are not persisted, so create -> read lifecycles cannot be verified; integration flows use stored data.
