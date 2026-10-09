import pytest

from helpers import brief

VALID_PRODUCT = {"title": "qa_auto product", "price": 13.5, "description": "created by API test",
                 "image": "https://i.pravatar.cc", "category": "electronics"}


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_013_create_product(api):
    r = api.post("/products", json=VALID_PRODUCT)
    assert r.status_code == 201, brief(r)
    body = r.json()
    assert isinstance(body.get("id"), int)
    for k, v in VALID_PRODUCT.items():
        assert body[k] == v


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_014_create_product_with_empty_body_returns_400(api):
    r = api.post("/products", json={})
    assert r.status_code == 400, f"a product with no data should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
@pytest.mark.parametrize("field,value", [("price", "abc"), ("price", -10), ("image", "not a url")],
                         ids=["text_price", "negative_price", "invalid_image_url"])
def test_FS_PRODUCTS_015_create_product_with_invalid_field_returns_400(api, field, value):
    r = api.post("/products", json={**VALID_PRODUCT, field: value})
    assert r.status_code == 400, f"{field}={value!r} should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_016_create_product_with_malformed_json_returns_400(api):
    r = api.post("/products", data="{bad json", headers={"Content-Type": "application/json"})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_017_malformed_json_error_is_returned_as_json(api):
    r = api.post("/products", data="{bad json", headers={"Content-Type": "application/json"})
    ctype = r.headers.get("content-type", "")
    assert ctype.startswith("application/json"), f"error body is {ctype!r}, not JSON: {r.text[:80]!r}"
