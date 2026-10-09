import pytest

from helpers import brief
from products.data import VALID_PRODUCT


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_010_update_product(api):
    r = api.put("/products/1", json=VALID_PRODUCT)
    assert r.status_code == 200, brief(r)
    assert r.json()["title"] == VALID_PRODUCT["title"]


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_011_update_nonexistent_product_returns_4xx(api):
    r = api.put("/products/9999", json=VALID_PRODUCT)
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_016_update_product_with_non_numeric_id_returns_400(api):
    r = api.put("/products/abc", json=VALID_PRODUCT)
    assert r.status_code == 400, brief(r)
