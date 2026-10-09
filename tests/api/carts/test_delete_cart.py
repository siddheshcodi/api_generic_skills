import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_006_delete_cart(api):
    r = api.delete("/carts/1")
    assert r.status_code == 200, brief(r)
