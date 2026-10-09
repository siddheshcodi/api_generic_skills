import pytest

from helpers import assert_schema, brief, jwt_claims


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_AUTH_001_login_with_valid_credentials(api, login_creds):
    r = api.post("/auth/login", json=login_creds)
    assert r.status_code == 200, f"spec documents 200 LoginResponse, got {r.status_code}"
    assert_schema(r.json(), "login_response")


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_AUTH_002_token_is_a_jwt_for_the_logged_in_user(api, token, login_creds):
    claims = jwt_claims(token)
    assert claims.get("user") == login_creds["username"], claims
    assert isinstance(claims.get("sub"), int)


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_AUTH_003_token_has_an_expiry(token):
    claims = jwt_claims(token)
    assert "exp" in claims, f"token has no 'exp' claim and never expires: claims {sorted(claims)}"


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_AUTH_004_login_with_wrong_password_returns_401(api, login_creds):
    r = api.post("/auth/login", json={**login_creds, "password": "wrong-password"})
    assert r.status_code == 401, brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_005_login_with_unknown_username_returns_401(api):
    r = api.post("/auth/login", json={"username": "qa_auto_nobody", "password": "whatever1"})
    assert r.status_code == 401, brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_006_password_is_case_sensitive(api, login_creds):
    r = api.post("/auth/login", json={**login_creds, "password": login_creds["password"].upper()})
    assert r.status_code == 401, brief(r)


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("body", [{}, {"username": "johnd"}], ids=["empty_body", "missing_password"])
def test_FS_AUTH_007_login_without_required_fields_returns_400(api, body):
    r = api.post("/auth/login", json=body)
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("body", [{"username": "' OR '1'='1", "password": "' OR '1'='1"}, {"username": 123, "password": 456}],
                         ids=["sql_like", "numbers"])
def test_FS_AUTH_008_login_with_malicious_or_wrong_type_input_is_rejected(api, body):
    r = api.post("/auth/login", json=body)
    assert r.status_code in (400, 401), brief(r)
    assert "token" not in r.text


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_009_login_with_non_json_body_returns_400(api):
    r = api.post("/auth/login", data="username=x", headers={"Content-Type": "text/plain"})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_010_login_errors_are_returned_as_json(api, login_creds):
    r = api.post("/auth/login", json={**login_creds, "password": "wrong-password"})
    ctype = r.headers.get("content-type", "")
    assert ctype.startswith("application/json"), f"error body is {ctype!r}, not JSON: {r.text[:60]!r}"


@pytest.mark.regression
@pytest.mark.negative
def test_FS_AUTH_011_get_on_login_route_is_not_allowed(api):
    r = api.get("/auth/login")
    assert r.status_code in (404, 405), brief(r)
