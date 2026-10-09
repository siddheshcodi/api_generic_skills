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
