import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_008_delete_user(api):
    r = api.delete("/users/1")
    assert r.status_code == 200, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_USERS_012_delete_nonexistent_user_returns_4xx(api):
    r = api.delete("/users/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"
