import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_020_delete_user(api):
    r = api.delete("/users/1")
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_021_delete_response_does_not_expose_password(api):
    assert "password" not in api.delete("/users/1").json(), "DELETE /users/1 response contains the password"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_022_delete_nonexistent_user_returns_4xx(api):
    assert_not_found(api.delete("/users/9999"))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_023_delete_user_non_integer_id_returns_400(api):
    r = api.delete("/users/abc")
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_024_delete_user_without_login_is_rejected(api):
    r = api.delete("/users/1")
    assert r.status_code in (401, 403), f"anyone can delete a user account without logging in: {brief(r)}"
