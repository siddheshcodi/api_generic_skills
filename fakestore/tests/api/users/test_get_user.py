import pytest

from helpers import assert_not_found, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_USERS_004_get_single_user(api):
    r = api.get("/users/1")
    assert r.status_code == 200, brief(r)
    assert_schema(r.json(), "user")
    assert r.json()["id"] == 1


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_USERS_005_get_nonexistent_user_returns_4xx(api):
    assert_not_found(api.get("/users/9999"))


@pytest.mark.regression
@pytest.mark.negative
def test_FS_USERS_006_get_user_non_integer_id_returns_400(api):
    r = api.get("/users/abc")
    assert r.status_code == 400, brief(r)


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_USERS_007_single_user_does_not_expose_password(api):
    r = api.get("/users/1")
    assert "password" not in r.json(), "GET /users/1 (no login needed) returns the user's password"
