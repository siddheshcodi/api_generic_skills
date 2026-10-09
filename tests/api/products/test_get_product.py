import pytest

from helpers import assert_json_object, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_PRODUCTS_004_get_single_product(api):
    r = api.get("/products/1")
    assert r.status_code == 200, brief(r)
    assert_json_object(r)
    assert_schema(r.json(), "product")
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.negative
def test_FS_PRODUCTS_005_get_nonexistent_product_is_not_empty_200(api):
    r = api.get("/products/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.negative
def test_FS_PRODUCTS_006_get_product_non_numeric_id_returns_400(api):
    r = api.get("/products/abc")
    assert r.status_code == 400, f"expected 400 for id 'abc' (spec: id is integer), got {brief(r)}"
