import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_015_update_user_email(api):
    r = api.put("/users/2", json={"email": "qa_auto@example.com"})
    assert r.status_code == 200, brief(r)
    assert r.json()["email"] == "qa_auto@example.com"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
@pytest.mark.parametrize("method", ["PUT", "PATCH"])
def test_FS_USERS_016_update_user_response_identifies_the_user(api, method):
    r = api.request(method, "/users/2", json={"username": "qa_auto_user"})
    assert r.status_code == 200, brief(r)
    assert r.json().get("id") == 2, f"spec: 200 returns the User; {method} response has no id: {r.json()}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_017_update_nonexistent_user_returns_4xx(api):
    assert_not_found(api.put("/users/9999", json={"email": "qa_auto@example.com"}))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_018_update_user_non_integer_id_returns_400(api):
    r = api.put("/users/abc", json={"email": "qa_auto@example.com"})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_019_update_user_with_invalid_email_returns_400(api):
    r = api.put("/users/2", json={"email": "bad"})
    assert r.status_code == 400, f"email 'bad' should be rejected, got {brief(r)}"
