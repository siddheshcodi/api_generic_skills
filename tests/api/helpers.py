import json
from pathlib import Path

from jsonschema import validate

SCHEMAS = Path(__file__).parent / "schemas"


def assert_schema(body, name):
    validate(instance=body, schema=json.loads((SCHEMAS / f"{name}.json").read_text()))


def assert_json_object(r):
    """200 must carry a real JSON object, not an empty body."""
    assert r.text.strip(), f"{r.request.method} {r.url} -> {r.status_code} with EMPTY body"
    assert isinstance(r.json(), dict), f"expected JSON object, got: {r.text[:200]}"


def brief(r):
    return f"{r.request.method} {r.url} -> {r.status_code}: {r.text[:200]!r}"
