import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_024_delete_product(api):
    r = api.delete("/products/1")
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_025_delete_nonexistent_product_returns_4xx(api):
    assert_not_found(api.delete("/products/9999"))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_026_delete_product_non_integer_id_returns_400(api):
    r = api.delete("/products/abc")
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_027_delete_product_without_login_is_rejected(api):
    r = api.delete("/products/1")
    assert r.status_code in (401, 403), f"anyone can delete a product without logging in: {brief(r)}"
