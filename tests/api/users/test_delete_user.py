import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_USERS_008_delete_user(api):
    r = api.delete("/users/1")
    assert r.status_code == 200, brief(r)
