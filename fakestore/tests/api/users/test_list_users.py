import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_USERS_001_list_all_users(api):
    r = api.get("/users")
    assert r.status_code == 200, brief(r)
    users = r.json()
    assert len(users) == 10
    for u in users:
        assert_schema(u, "user")


@pytest.mark.regression
@pytest.mark.positive
def test_FS_USERS_002_limit_and_sort_users(api):
    users = api.get("/users?limit=3&sort=desc").json()
    assert [u["id"] for u in users] == [10, 9, 8]


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_USERS_003_user_list_does_not_expose_passwords(api):
    leaked = [u["id"] for u in api.get("/users").json() if "password" in u]
    assert not leaked, f"GET /users (no login needed) returns 'password' for user ids {leaked}"
