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
