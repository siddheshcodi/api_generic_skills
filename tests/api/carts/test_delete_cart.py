import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_006_delete_cart(api):
    r = api.delete("/carts/1")
    assert r.status_code == 200, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_010_delete_nonexistent_cart_returns_4xx(api):
    r = api.delete("/carts/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"
