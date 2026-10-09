import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_005_update_cart(api):
    items = [{"productId": 2, "quantity": 3}]
    r = api.put("/carts/1", json={"userId": 1, "products": items})
    assert r.status_code == 200, brief(r)
    assert r.json().get("products") == items


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_009_update_nonexistent_cart_returns_4xx(api):
    r = api.put("/carts/9999", json={"userId": 1, "products": [{"productId": 1, "quantity": 1}]})
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"
