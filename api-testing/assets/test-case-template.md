# Test cases — <Project>

Generated from `test-cases.json` by `scripts/test_report.py --plan-only` — edit the JSON, not this
file. Layout of the generated file:

## Coverage summary
| Module | Endpoints | Positive | Negative | Total |
|---|---|---|---|---|
| Users | 3 | 4 | 7 | 11 |

## Users
Endpoints: `POST /users`, `GET /users`, `GET /users/{id}`

### Positive scenarios (4)
| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| API-USERS-001 | Create user with required fields | `POST /users` | Happy path | P0 | `{"name","email"}` | 201; body has id, email = sent email; matches user schema |

### Negative scenarios (7)
| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |
|---|---|---|---|---|---|---|
| API-USERS-004 | Create user without email | `POST /users` | Validation | P1 | `{"name"}` | 400/422 with message mentioning "email"; no 5xx |
| API-USERS-010 | List users without token | `GET /users` | Auth | P0 | no Authorization | 401 |

## Assumptions and open questions
- (assumed) Duplicate email returns 409 — spec does not say. Confirm with: <who>
