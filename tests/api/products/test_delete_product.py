import pytest

from helpers import brief


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_012_delete_product(api):
    r = api.delete("/products/1")
    assert r.status_code == 200, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_013_delete_nonexistent_product_returns_4xx(api):
    r = api.delete("/products/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_017_delete_product_with_non_numeric_id_returns_400(api):
    r = api.delete("/products/abc")
    assert r.status_code == 400, brief(r)
