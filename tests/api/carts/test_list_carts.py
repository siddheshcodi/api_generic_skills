import pytest

from helpers import brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_CARTS_001_list_all_carts(api):
    r = api.get("/carts")
    assert r.status_code == 200, brief(r)
    assert isinstance(r.json(), list) and r.json()
