"""Flow: Auth -> Users -> Carts. A logged-in user can be found and owns at least one cart."""
import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_001_logged_in_user_has_profile_and_own_carts(api, login_creds):
    login = api.post("/auth/login", json=login_creds)
    assert login.status_code in (200, 201), brief(login)  # exact code is checked by FS-AUTH-001
    assert login.json().get("token"), "login returned no token"

    users = api.get("/users").json()
    me = next((u for u in users if u.get("username") == login_creds["username"]), None)
    assert me, f"user '{login_creds['username']}' can log in but is not in GET /users"

    carts = [c for c in api.get("/carts").json() if c.get("userId") == me["id"]]
    assert carts, f"user id {me['id']} has no carts"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_005_login_token_identifies_the_same_user(api, login_creds):
    import base64
    import json as _json
    token = api.post("/auth/login", json=login_creds).json()["token"]
    payload = token.split(".")[1]
    claims = _json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    me = next(u for u in api.get("/users").json() if u["username"] == login_creds["username"])
    assert claims.get("sub") == me["id"], f"token sub={claims.get('sub')} but user id is {me['id']}"
