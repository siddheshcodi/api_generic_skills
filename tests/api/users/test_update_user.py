import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_007_update_user(api, unique):
    name = unique()
    r = api.put("/users/1", json={"username": name})
    assert r.status_code == 200, brief(r)
    assert r.json().get("username") == name


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_011_update_nonexistent_user_returns_4xx(api, unique):
    r = api.put("/users/9999", json={"username": unique()})
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"
