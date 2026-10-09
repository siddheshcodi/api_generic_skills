import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_020_update_cart_with_put(api):
    r = api.put("/carts/1", json={"userId": 1, "products": [{"productId": 2, "quantity": 3}]})
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1 and r.json()["products"] == [{"productId": 2, "quantity": 3}]


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_021_update_cart_with_patch(api):
    r = api.patch("/carts/1", json={"products": [{"productId": 5, "quantity": 1}]})
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_022_update_nonexistent_cart_returns_4xx(api):
    assert_not_found(api.put("/carts/9999", json={"userId": 1, "products": [{"productId": 1, "quantity": 1}]}))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_023_update_cart_non_integer_id_returns_400(api):
    r = api.put("/carts/abc", json={"userId": 1})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_024_update_cart_with_negative_quantity_returns_400(api):
    r = api.put("/carts/1", json={"userId": 1, "products": [{"productId": 1, "quantity": -5}]})
    assert r.status_code == 400, f"quantity -5 should be rejected, got {brief(r)}"
