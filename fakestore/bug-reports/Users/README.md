# Users: 16 bugs

🔴 Critical 3 · 🟠 High 1 · 🟡 Medium 12 · 🟢 Low 0

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-USERS-01](BUG-USERS-01.md) | 🔴 Critical | P1 | User list returns every user's password without login | `GET /users` | FS-USERS-003 | BUG-001 |
| [BUG-USERS-02](BUG-USERS-02.md) | 🔴 Critical | P1 | Single user returns the password without login | `GET /users/{id}` | FS-USERS-007 | BUG-001 |
| [BUG-USERS-03](BUG-USERS-03.md) | 🔴 Critical | P1 | Delete user response returns the password | `DELETE /users/{id}` | FS-USERS-021 | BUG-001 |
| [BUG-USERS-04](BUG-USERS-04.md) | 🟠 High | P1 | Anyone can delete a user account without logging in | `DELETE /users/{id}` | FS-USERS-024 | BUG-002 |
| [BUG-USERS-05](BUG-USERS-05.md) | 🟡 Medium | P2 | Get user 9999 returns 200 'null' instead of 404 | `GET /users/{id}` | FS-USERS-005 | BUG-005 |
| [BUG-USERS-06](BUG-USERS-06.md) | 🟡 Medium | P3 | Create user response returns only an id, not the user | `POST /users` | FS-USERS-009 | BUG-009 |
| [BUG-USERS-07](BUG-USERS-07.md) | 🟡 Medium | P2 | New users are often given the id of an existing user (id 1) | `POST /users` | FS-USERS-010 | BUG-004 |
| [BUG-USERS-08](BUG-USERS-08.md) | 🟡 Medium | P2 | Create user accepted with an empty body | `POST /users` | FS-USERS-011 | BUG-006 |
| [BUG-USERS-09](BUG-USERS-09.md) | 🟡 Medium | P2 | Create user accepts an invalid email | `POST /users` | FS-USERS-012 | BUG-006 |
| [BUG-USERS-10](BUG-USERS-10.md) | 🟡 Medium | P2 | Create user accepted without a password | `POST /users` | FS-USERS-013 | BUG-006 |
| [BUG-USERS-11](BUG-USERS-11.md) | 🟡 Medium | P3 | Create user accepts an existing username | `POST /users` | FS-USERS-014 | BUG-007 |
| [BUG-USERS-12](BUG-USERS-12.md) | 🟡 Medium | P3 | PATCH user response has no user id | `PUT, PATCH /users/{id}` | FS-USERS-016 | BUG-009 |
| [BUG-USERS-13](BUG-USERS-13.md) | 🟡 Medium | P3 | PUT user response has no user id | `PUT, PATCH /users/{id}` | FS-USERS-016 | BUG-009 |
| [BUG-USERS-14](BUG-USERS-14.md) | 🟡 Medium | P2 | Update user 9999 returns 200 instead of 404 | `PUT /users/{id}` | FS-USERS-017 | BUG-005 |
| [BUG-USERS-15](BUG-USERS-15.md) | 🟡 Medium | P2 | Update user accepts an invalid email | `PUT /users/{id}` | FS-USERS-019 | BUG-006 |
| [BUG-USERS-16](BUG-USERS-16.md) | 🟡 Medium | P2 | Delete user 9999 returns 200 'null' instead of 404 | `DELETE /users/{id}` | FS-USERS-022 | BUG-005 |

[← All bugs](../README.md)
