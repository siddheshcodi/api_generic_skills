import os
import uuid
from pathlib import Path

import pytest
import yaml

from client import ApiClient

ROOT = Path(__file__).resolve().parents[2]
CONFIG = yaml.safe_load((ROOT / "api-test.config.yaml").read_text(encoding="utf-8"))
ENV_NAME = os.getenv("API_ENV", CONFIG["environments"]["default"])
ENV = CONFIG["environments"][ENV_NAME]


def _env(name):
    value = os.getenv(name or "")
    if not value:
        pytest.skip(f"Environment variable {name} is not set")
    return value


@pytest.fixture(scope="session")
def config():
    return CONFIG


@pytest.fixture(scope="session")
def api():
    headers = dict(CONFIG.get("defaults", {}).get("default_headers", {}))
    return ApiClient(ENV["base_url"], headers, CONFIG.get("defaults", {}).get("timeout_seconds", 30))


@pytest.fixture(scope="session")
def login_creds():
    l = CONFIG["auth"]["login_endpoint"]
    return {"username": _env(l["username_env"]), "password": _env(l["password_env"])}


@pytest.fixture
def unique():
    prefix = CONFIG.get("testing", {}).get("test_data_prefix", "qa_auto_")
    return lambda: f"{prefix}{uuid.uuid4().hex[:8]}"


MODULE_FOLDERS = {"products", "carts", "users", "auth", "integration"}
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
