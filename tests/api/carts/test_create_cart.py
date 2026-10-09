import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_004_create_cart(api):
    r = api.post("/carts", json={"userId": 1, "products": [{"id": 1}]})
    assert r.status_code == 201, brief(r)
    assert isinstance(r.json().get("id"), int)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_007_create_cart_with_empty_body_returns_400(api):
    r = api.post("/carts", json={})
    assert r.status_code == 400, f"expected 400 for empty cart (no userId/products), got {brief(r)}"
