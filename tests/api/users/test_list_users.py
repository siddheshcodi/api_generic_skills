import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_USERS_001_list_all_users(api):
    r = api.get("/users")
    assert r.status_code == 200, brief(r)
    for u in r.json():
        assert_schema(u, "user")


@pytest.mark.regression
@pytest.mark.negative
def test_FS_USERS_003_user_responses_do_not_expose_passwords(api):
    leaked = [u["id"] for u in api.get("/users").json() if "password" in u]
    assert not leaked, f"GET /users returns a password field for user ids {leaked} (no auth needed)"
