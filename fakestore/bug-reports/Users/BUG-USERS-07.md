# BUG-USERS-07: New users are often given the id of an existing user (id 1)

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-07 |
| **Module** | Users |
| **Severity** | 🟡 Medium |
| **Priority** | P2 |
| **Status** | Open |
| **Endpoint** | `POST /users` |
| **Test case** | FS-USERS-010 (negative, Data integrity) |
| **Root cause** | BUG-004: POST /users gives a new user the id of an existing user (id 1) in about 40% of calls |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 runs (8/20 single creates) |
| **Found on** | 2026-10-09 |

## Summary
Test: New user never gets an existing users id. Expected **no new user gets an existing user's id (1-10)**. Instead: 5 new users got ids [1, 11, 11, 11, 1]; 2 reuse an existing user's id

## Why it matters
When a new customer signs up, the system often gives them the same customer number as an existing customer (number 1). Two people with the same number means one could see or change the other's orders and data. Every new account must get its own unique number.

## Steps to reproduce
1. Send `POST https://fakestoreapi.com/users` and body `{"username":"qa_auto_x","email":"qa_auto_x@example.com","password":"<PASSWORD>"}  (repeat 5-20 times)`
2. Check the status code and response body.

```bash
curl -s -X POST 'https://fakestoreapi.com/users' -H 'Content-Type: application/json' -d '{"username":"qa_auto_x","email":"qa_auto_x@example.com","password":"<PASSWORD>"}  (repeat 5-20 times)'
```

## Expected result
no new user gets an existing user's id (1-10)

## Actual result
5 new users got ids [1, 11, 11, 11, 1]; 2 reuse an existing user's id

## Test reference
- Test: `tests/api/users/test_create_user.py::test_FS_USERS_010_new_user_never_gets_an_existing_users_id`
- Failure message: `5 new users got ids [1, 11, 11, 11, 1]; 2 reuse an existing user's id`

[← Users bugs](README.md) · [All bugs](../README.md)
