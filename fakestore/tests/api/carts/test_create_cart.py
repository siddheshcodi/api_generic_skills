import pytest

from helpers import brief

VALID_CART = {"userId": 1, "date": "2026-10-09", "products": [{"productId": 1, "quantity": 2}]}


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_013_create_cart(api):
    r = api.post("/carts", json=VALID_CART)
    assert r.status_code == 201, brief(r)
    body = r.json()
    assert isinstance(body.get("id"), int) and body["userId"] == 1 and body["products"] == VALID_CART["products"]


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_014_create_cart_with_empty_body_returns_400(api):
    r = api.post("/carts", json={})
    assert r.status_code == 400, f"a cart with no user or products should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.parametrize("override", [{"userId": "abc"}, {"products": "x"}, {"date": "notadate"}],
                         ids=["text_user_id", "products_not_list", "invalid_date"])
def test_FS_CARTS_015_create_cart_with_wrong_types_returns_400(api, override):
    r = api.post("/carts", json={**VALID_CART, **override})
    assert r.status_code == 400, f"{override} should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_016_create_cart_for_unknown_user_is_rejected(api):
    r = api.post("/carts", json={**VALID_CART, "userId": 9999})
    assert r.status_code in (400, 404), f"user 9999 does not exist, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_017_create_cart_with_unknown_product_is_rejected(api):
    r = api.post("/carts", json={**VALID_CART, "products": [{"productId": 99999, "quantity": 1}]})
    assert r.status_code in (400, 404), f"product 99999 does not exist, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.parametrize("qty", [-2, 0], ids=["negative", "zero"])
def test_FS_CARTS_018_create_cart_with_invalid_quantity_returns_400(api, qty):
    r = api.post("/carts", json={**VALID_CART, "products": [{"productId": 1, "quantity": qty}]})
    assert r.status_code == 400, f"quantity {qty} should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_019_create_cart_without_login_is_rejected(api):
    r = api.post("/carts", json=VALID_CART)
    assert r.status_code in (401, 403), f"anyone can create a cart for user 1 without logging in: {brief(r)}"
