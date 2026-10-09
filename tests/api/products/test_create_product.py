import pytest

from helpers import brief
from products.data import VALID_PRODUCT


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_007_create_product(api):
    r = api.post("/products", json=VALID_PRODUCT)
    assert r.status_code == 201, brief(r)
    body = r.json()
    assert isinstance(body.get("id"), int)
    for k, v in VALID_PRODUCT.items():
        assert body[k] == v, f"{k}: sent {v!r}, got {body.get(k)!r}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_008_create_product_with_empty_body_returns_400(api):
    r = api.post("/products", json={})
    assert r.status_code == 400, f"expected 400 for empty body (requestBody required), got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_009_create_product_malformed_json_returns_400(api):
    r = api.post("/products", data="not json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_014_create_product_with_text_price_returns_400(api):
    r = api.post("/products", json={**VALID_PRODUCT, "price": "abc"})
    assert r.status_code == 400, f"expected 400 for price 'abc' (spec: number), got {brief(r)}"
