# Framework: Python + Pytest + requests

Best default for new suites: readable, quick to learn, great for freshers.
If the project already has API tests, follow their existing structure instead of this layout.

## Dependencies (`requirements-test.txt`)
```
pytest>=8
requests>=2.31
jsonschema>=4
pyyaml>=6
pytest-html>=4      # optional HTML report
```

## Layout — folder per module, file per operation
```
tests/api/
├── conftest.py              # config, auth, client, cleanup fixtures + marker rules
├── client.py                # thin wrapper around requests
├── helpers.py               # assert_schema and small shared helpers
├── schemas/                 # JSON schemas (from OpenAPI components)
│   └── user.json
├── users/                   # one folder per module (resource / OpenAPI tag)
│   ├── __init__.py
│   ├── data.py              # optional: shared test data for this module
│   ├── test_list_users.py   # GET /users            positive + negative
│   ├── test_get_user.py     # GET /users/{id}
│   ├── test_create_user.py  # POST /users
│   ├── test_update_user.py  # PUT/PATCH /users/{id}
│   └── test_delete_user.py  # DELETE /users/{id}
├── orders/ ...
└── integration/             # cross-module flows (login -> order -> pay, data consistency)
    ├── __init__.py
    └── test_order_flow.py
pytest.ini
```
- Positive and negative tests of one operation stay in the **same file**; the type is a marker.
- File names must be unique across folders (`test_get_user.py`, not `test_get.py` in each).
- Tiny APIs may start with one `test_<module>.py` per module and move to folders as they grow.

## pytest.ini
```ini
[pytest]
testpaths = tests/api
pythonpath = tests/api
markers =
    smoke: fast critical checks (P0/P1)
    regression: full coverage
    destructive: creates/updates/deletes data
    positive: valid input, expects success
    negative: invalid input / unknown ids / wrong auth, expects a clean error
    integration: cross-module flows (auto-applied from folder)
    users: Users module (auto-applied from folder)
    orders: Orders module (auto-applied from folder)
addopts = -ra
```

## client.py
```python
import time
import requests


class ApiClient:
    """Small wrapper: base URL, default headers, timeout, timing."""

    def __init__(self, base_url, headers=None, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.timeout = timeout

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        start = time.perf_counter()
        resp = self.session.request(method, f"{self.base_url}{path}", **kwargs)
        resp.elapsed_ms = round((time.perf_counter() - start) * 1000)
        return resp

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def patch(self, path, **kw):  return self.request("PATCH", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
```

## conftest.py (reads api-test.config.yaml — no project values hard-coded)
```python
import base64
import json
import os
import uuid
from pathlib import Path

import pytest
import requests
import yaml

from client import ApiClient  # adjust import to your layout

ROOT = Path(__file__).resolve().parents[2]
CONFIG = yaml.safe_load((ROOT / "api-test.config.yaml").read_text())
ENV_NAME = os.getenv("API_ENV", CONFIG["environments"]["default"])
ENV = CONFIG["environments"][ENV_NAME]


def _env(name):
    value = os.getenv(name or "")
    if not value:
        pytest.exit(f"Environment variable {name} is not set", returncode=3)
    return value


def _auth_headers():
    auth = CONFIG.get("auth", {})
    kind = auth.get("type", "none")
    if kind == "none":
        return {}
    if kind == "bearer":
        return {"Authorization": f"Bearer {_env(auth['bearer']['token_env'])}"}
    if kind == "basic":
        b = auth["basic"]
        raw = f"{_env(b['username_env'])}:{_env(b['password_env'])}".encode()
        return {"Authorization": "Basic " + base64.b64encode(raw).decode()}
    if kind == "api_key":
        k = auth["api_key"]
        return {k["header"]: _env(k["value_env"])}
    if kind == "oauth2_client_credentials":
        o = auth["oauth2_client_credentials"]
        r = requests.post(o["token_url"], data={
            "grant_type": "client_credentials",
            "client_id": _env(o["client_id_env"]),
            "client_secret": _env(o["client_secret_env"]),
            "scope": o.get("scope", ""),
        }, timeout=30)
        r.raise_for_status()
        return {"Authorization": f"Bearer {r.json()['access_token']}"}
    if kind == "login_endpoint":
        l = auth["login_endpoint"]
        body = l["body_template"].replace("{username}", _env(l["username_env"])) \
                                 .replace("{password}", _env(l["password_env"]))
        r = requests.request(l.get("method", "POST"), ENV["base_url"].rstrip("/") + l["path"],
                             json=json.loads(body), timeout=30)
        r.raise_for_status()
        token = r.json()
        for part in l["token_json_path"].split("."):
            token = token[part]
        return {l.get("header", "Authorization"): f"{l.get('prefix', 'Bearer ')}{token}"}
    raise ValueError(f"Unknown auth type: {kind}")


@pytest.fixture(scope="session")
def config():
    return CONFIG


@pytest.fixture(scope="session")
def is_production():
    return bool(ENV.get("is_production"))


@pytest.fixture(scope="session")
def api():
    """Authenticated client."""
    headers = dict(CONFIG.get("defaults", {}).get("default_headers", {}))
    headers.update(_auth_headers())
    return ApiClient(ENV["base_url"], headers, CONFIG.get("defaults", {}).get("timeout_seconds", 30))


@pytest.fixture(scope="session")
def anon_api():
    """Client WITHOUT auth — for 401 tests."""
    headers = dict(CONFIG.get("defaults", {}).get("default_headers", {}))
    return ApiClient(ENV["base_url"], headers)


@pytest.fixture
def unique():
    """Unique, prefixed test value, e.g. qa_auto_3f9a1c."""
    prefix = CONFIG.get("testing", {}).get("test_data_prefix", "qa_auto_")
    return lambda: f"{prefix}{uuid.uuid4().hex[:8]}"


@pytest.fixture
def cleanup(api):
    """Register paths to DELETE after the test: cleanup.append('/users/123')."""
    paths = []
    yield paths
    if CONFIG.get("testing", {}).get("cleanup_test_data", True):
        for p in reversed(paths):
            api.delete(p)


MODULE_FOLDERS = {"users", "orders", "integration"}   # = folders under tests/api, register in pytest.ini
TYPE_MARKERS = {"positive", "negative"}


def pytest_collection_modifyitems(config, items):
    """Tag each test with its module folder; require a positive/negative marker; protect production."""
    allow = CONFIG.get("testing", {}).get("allow_destructive_on_production", False)
    untyped = []
    for item in items:
        folder = Path(str(item.fspath)).parent.name
        if folder in MODULE_FOLDERS:
            item.add_marker(getattr(pytest.mark, folder))
        if not TYPE_MARKERS & set(item.keywords):
            untyped.append(item.nodeid)
        if ENV.get("is_production") and not allow and "destructive" in item.keywords:
            item.add_marker(pytest.mark.skip(reason="destructive test skipped on production"))
    if untyped:
        raise pytest.UsageError("Every test needs @pytest.mark.positive or @pytest.mark.negative:\n  "
                                + "\n  ".join(untyped))
```

## Schema helper (`helpers.py`)
```python
import json
from pathlib import Path

from jsonschema import validate

SCHEMAS = Path(__file__).parent / "schemas"

def assert_schema(body, name):
    validate(instance=body, schema=json.loads((SCHEMAS / f"{name}.json").read_text()))
```
Build schema files from OpenAPI `components.schemas` (convert `$ref`s to inline or use
`referencing` registry). Set `"additionalProperties": false` only if the API contract is strict.

## Example tests (`users/test_create_user.py`, `users/test_list_users.py`) — ID + type marker on every test
```python
import pytest

from helpers import assert_schema


# users/test_create_user.py
@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_API_USERS_001_create_user_with_required_fields(api, unique, cleanup):
    payload = {"name": unique(), "email": f"{unique()}@example.com"}
    r = api.post("/users", json=payload)
    assert r.status_code == 201, r.text
    body = r.json()
    cleanup.append(f"/users/{body['id']}")
    assert body["email"] == payload["email"]
    assert_schema(body, "user")


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("missing", ["name", "email"])
def test_API_USERS_004_create_user_missing_required_field(api, unique, missing):
    payload = {"name": unique(), "email": f"{unique()}@example.com"}
    payload.pop(missing)
    r = api.post("/users", json=payload)
    assert r.status_code in (400, 422), f"expected 400/422, got {r.status_code}: {r.text[:300]}"


# users/test_list_users.py
@pytest.mark.smoke
@pytest.mark.negative
def test_API_USERS_010_get_users_without_token_returns_401(anon_api):
    assert anon_api.get("/users").status_code == 401
```
```python
# integration/test_order_flow.py — cross-module flow, own data, cleaned up
@pytest.mark.regression
@pytest.mark.positive
def test_API_INTEG_001_user_can_order_an_existing_product(api, unique, cleanup):
    product = api.get("/products", params={"limit": 1}).json()[0]
    r = api.post("/orders", json={"productId": product["id"], "quantity": 1})
    assert r.status_code == 201, r.text
    cleanup.append(f"/orders/{r.json()['id']}")
    assert api.get(f"/orders/{r.json()['id']}").json()["productId"] == product["id"]
```
Assertion messages should include status and a body excerpt — that text flows into JUnit XML and
saves triage time.

## Run commands
```bash
pip install -r requirements-test.txt
pytest -m smoke --junitxml=api-test-reports/junit.xml                 # smoke
pytest --junitxml=api-test-reports/junit.xml --html=api-test-reports/report.html   # full
API_ENV=staging pytest -m smoke --junitxml=api-test-reports/junit.xml # other env
pytest -k API_USERS_004 -v                                            # rerun one case
pytest -m negative                                                    # all negative tests
pytest -m "users and negative"                                        # one module, one type
pytest -m integration                                                 # cross-module flows only
pytest tests/api/users                                                # one module by folder
```
Then: `python <skill>/scripts/parse_results.py api-test-reports/junit.xml --out api-test-reports/results`
