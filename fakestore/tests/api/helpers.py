import base64
import json
import re
from pathlib import Path

from jsonschema import validate

SCHEMAS = Path(__file__).parent / "schemas"
EXISTING_USER_IDS = range(1, 11)    # the 10 seeded users


def assert_schema(body, name):
    validate(instance=body, schema=json.loads((SCHEMAS / f"{name}.json").read_text()))


def assert_not_found(r):
    """Unknown or invalid id: the spec documents 400 'Bad request'; 404 is also acceptable. Never an empty 200."""
    assert r.status_code in (400, 404), f"expected 400/404 for unknown/invalid id, got {brief(r)}"


def jwt_claims(token):
    payload = token.split(".")[1]
    return json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))


def mask(text):
    """Hide tokens and credential values so failure messages are safe to store in reports."""
    text = re.sub(r"eyJ[\w.-]+", "<JWT>", text)
    return re.sub(r'"(password)":"[^"]*"', r'"\1":"<MASKED>"', text)


def brief(r):
    return f"{r.request.method} {r.url} -> {r.status_code}: {mask(r.text[:200])!r}"
