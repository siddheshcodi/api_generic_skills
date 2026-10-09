# BUG-USERS-04: Anyone can delete a user account without logging in

| Field | Value |
|---|---|
| **Bug ID** | BUG-USERS-04 |
| **Module** | Users |
| **Severity** | 🟠 High |
| **Priority** | P1 |
| **Status** | Open |
| **Endpoint** | `DELETE /users/{id}` |
| **Test case** | FS-USERS-024 (negative, Security) |
| **Root cause** | BUG-002: Products, carts and users can be created, changed and deleted without logging in |
| **Environment** | public (https://fakestoreapi.com) |
| **Reproducibility** | 3/3 |
| **Found on** | 2026-10-09 |

## Summary
Test: Delete user without login is rejected. Expected **401/403**. Got HTTP **200**.

## Why it matters
Anyone, without logging in, can delete products, delete customer accounts, or create shopping carts in another customer's name. Changing data should only be allowed for logged-in people who own the data or are administrators. Right now any visitor or script could wipe or tamper with the store.

## Steps to reproduce
1. Send `DELETE https://fakestoreapi.com/users/1`
2. Check the status code and response body.

```bash
curl -s -X DELETE 'https://fakestoreapi.com/users/1'
```

## Expected result
401/403

## Actual result
HTTP **200**, body: `{"address":{"geolocation":{"lat":"-37.3159","long":"81.1496"},"city":"kilcoole","street":"new road","number":7682,"zipcode":"12926-3874"},"id":1,"email":"john@gmail.com","username":"johnd","password":`

## Test reference
- Test: `tests/api/users/test_delete_user.py::test_FS_USERS_024_delete_user_without_login_is_rejected`
- Failure message: `anyone can delete a user account without logging in: DELETE https://fakestoreapi.com/users/1 -> 200: '{"address":{"geolocation":{"lat":"-37.3159","long":"81.1496"},"city":"kilcoole","street":"new road","number":7682,"zipcode":"12926-3874"},"id":1,"email":"john@gmail.com","username":"johnd","password":'`

[← Users bugs](README.md) · [All bugs](../README.md)
