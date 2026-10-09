import pytest

from helpers import assert_json_object, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_USERS_002_get_single_user(api):
    r = api.get("/users/1")
    assert r.status_code == 200, brief(r)
    assert_json_object(r)
    assert_schema(r.json(), "user")


@pytest.mark.regression
@pytest.mark.negative
def test_FS_USERS_004_get_nonexistent_user_is_not_empty_200(api):
    r = api.get("/users/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.parametrize("method", ["GET", "DELETE"])
def test_FS_USERS_009_single_user_responses_do_not_expose_password(api, method):
    r = api.request(method, "/users/1")
    assert "password" not in (r.json() or {}), f"{method} /users/1 response contains a password field"
