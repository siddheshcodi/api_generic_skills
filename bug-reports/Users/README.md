# Users: 9 bugs

Critical 3 · High 0 · Medium 6 · Low 0

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-USERS-01](BUG-USERS-01.md) | 🔴 Critical | P1 | User list must not expose passwords | `GET /users` | FS-USERS-003 | BUG-001 |
| [BUG-USERS-02](BUG-USERS-02.md) | 🔴 Critical | P1 | Single-user responses must not expose password (DELETE) | `DELETE /users/{id}` | FS-USERS-009 | BUG-001 |
| [BUG-USERS-03](BUG-USERS-03.md) | 🔴 Critical | P1 | Single-user responses must not expose password (GET) | `GET /users/{id}` | FS-USERS-009 | BUG-001 |
| [BUG-USERS-04](BUG-USERS-04.md) | 🟠 Medium | P2 | Get a user that does not exist | `GET /users/{id}` | FS-USERS-004 | BUG-002 |
| [BUG-USERS-05](BUG-USERS-05.md) | 🟠 Medium | P3 | Create a user with an invalid email | `POST /users` | FS-USERS-006 | BUG-004 |
| [BUG-USERS-06](BUG-USERS-06.md) | 🟠 Medium | P2 | Update a user that does not exist | `PUT /users/{id}` | FS-USERS-011 | BUG-002 |
| [BUG-USERS-07](BUG-USERS-07.md) | 🟠 Medium | P2 | Delete a user that does not exist | `DELETE /users/{id}` | FS-USERS-012 | BUG-002 |
| [BUG-USERS-08](BUG-USERS-08.md) | 🟠 Medium | P3 | Create a user with an empty body | `POST /users` | FS-USERS-013 | BUG-004 |
| [BUG-USERS-09](BUG-USERS-09.md) | 🟠 Medium | P3 | Create a user without a password | `POST /users` | FS-USERS-014 | BUG-004 |

[← All bugs](../README.md)
