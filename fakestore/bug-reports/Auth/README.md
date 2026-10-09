# Auth: 3 bugs

🔴 Critical 0 · 🟠 High 1 · 🟡 Medium 0 · 🟢 Low 2

| Bug | Severity | Priority | Title | Endpoint | Test case | Root cause |
|---|---|---|---|---|---|---|
| [BUG-AUTH-01](BUG-AUTH-01.md) | 🟠 High | P2 | Login token never expires (no 'exp' claim) | `POST /auth/login` | FS-AUTH-003 | BUG-003 |
| [BUG-AUTH-02](BUG-AUTH-02.md) | 🟢 Low | P4 | Login returns 201 instead of the documented 200 | `POST /auth/login` | FS-AUTH-001 | BUG-011 |
| [BUG-AUTH-03](BUG-AUTH-03.md) | 🟢 Low | P3 | Login errors are plain text, not JSON | `POST /auth/login` | FS-AUTH-010 | BUG-010 |

[← All bugs](../README.md)
