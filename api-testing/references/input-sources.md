# Input sources — how to understand the API

Goal of Step 2: a clear **endpoint inventory** (what exists, what it needs, what it returns) and a
list of **open questions**. Use whichever sources the project has; combine them if several exist.

## 1. OpenAPI / Swagger (best source)
- Formats: `openapi.yaml|json` (v3.x) or `swagger.json|yaml` (v2.0). Often served at
  `/swagger.json`, `/v3/api-docs`, `/openapi.json`, `/api-docs`.
- Run `python scripts/api_inventory.py <file> --out <reports_dir>/inventory`.
- Use from the spec: required params and body fields, enums, min/max lengths and values, formats
  (email, uuid, date-time), response codes, response schemas, security schemes.
- Watch for: endpoints with no documented error responses (ask what they should return), `$ref`
  schemas you will reuse for schema validation, deprecated endpoints (lower priority).

## 2. Postman collection
- Export as **Collection v2.1** JSON. Environment files hold variables like `{{baseUrl}}` — map
  them to `environments.*.base_url` in config; never copy secret values into the config.
- Run the same inventory script; it understands Postman collections.
- Existing Postman test scripts (`pm.test(...)`) show what the team already checks — reuse those
  expectations, then add the gaps from the checklist.
- Example responses saved in the collection are a good source for expected shapes, but confirm
  they are current.

## 3. cURL commands
- Parse each command: method (`-X`, default GET, POST if `-d` present), URL and query, headers
  (`-H`), body (`-d`, `--data-raw`, `-F` for multipart), auth (`-u`, `Authorization` header).
- Replace any real token in what you write back with `<TOKEN>`.
- One cURL shows one happy path only. Ask for, or infer and label as assumption: required fields,
  validation rules, error codes.

## 4. Plain docs / Confluence page / README / verbal description
- Build the inventory manually with these columns:
  `Method | Path | Purpose | Auth | Path/query params | Body fields (required*) | Success code | Error codes | Notes`
- Mark every rule you inferred as **(assumed)** so the user can confirm.

## 5. No documentation at all
- Ask for one working example request (cURL or Postman) per endpoint.
- If allowed and running in Claude Code, call the endpoint once and record the real response as a
  baseline — but tell the user that tests built on observed behaviour only prove consistency, not
  correctness.

## Open questions to always resolve (or list as assumptions)
- Auth: how to get a token, how long it lives, roles that exist.
- Error format: is there a standard error body (`{code, message, details}`)?
- Pagination style (page/size, offset/limit, cursor) and max page size.
- Idempotency and duplicate handling for create endpoints.
- Rate limits.
- Which environments are safe for write/delete tests.
