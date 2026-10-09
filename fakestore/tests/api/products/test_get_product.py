import pytest

from helpers import assert_not_found, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_PRODUCTS_006_get_single_product(api):
    r = api.get("/products/1")
    assert r.status_code == 200, brief(r)
    assert_schema(r.json(), "product")
    assert r.json()["id"] == 1


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_PRODUCTS_007_get_nonexistent_product_returns_4xx(api):
    assert_not_found(api.get("/products/9999"))


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("pid", ["0", "-1"], ids=["zero", "negative"])
def test_FS_PRODUCTS_008_get_product_out_of_range_id_returns_4xx(api, pid):
    assert_not_found(api.get(f"/products/{pid}"))


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("pid", ["abc", "1.5"], ids=["text", "decimal"])
def test_FS_PRODUCTS_009_get_product_non_integer_id_returns_400(api, pid):
    r = api.get(f"/products/{pid}")
    assert r.status_code == 400, f"spec: id is an integer; expected 400 for {pid!r}, got {brief(r)}"
