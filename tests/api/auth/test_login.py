import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_AUTH_001_login_with_valid_credentials(api, login_creds):
    r = api.post("/auth/login", json=login_creds)
    assert r.status_code == 200, f"spec documents 200 LoginResponse, got {r.status_code}"
    assert_schema(r.json(), "login_response")


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_AUTH_002_login_with_wrong_password_returns_401(api, login_creds):
    r = api.post("/auth/login", json={**login_creds, "password": "wrong-password"})
    assert r.status_code == 401, brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_003_login_with_empty_body_returns_400(api):
    r = api.post("/auth/login", json={})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_004_login_sql_like_input_is_rejected_cleanly(api):
    r = api.post("/auth/login", json={"username": "' OR '1'='1", "password": "' OR '1'='1"})
    assert r.status_code in (400, 401), brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_005_login_with_unknown_username_returns_401(api):
    r = api.post("/auth/login", json={"username": "qa_auto_nobody", "password": "whatever1"})
    assert r.status_code == 401, brief(r)
