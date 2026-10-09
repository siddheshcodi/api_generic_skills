import pytest

from helpers import assert_not_found, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_CARTS_009_get_single_cart(api):
    r = api.get("/carts/1")
    assert r.status_code == 200, brief(r)
    assert_schema(r.json(), "cart")
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.positive
def test_FS_CARTS_010_single_cart_matches_spec_schema(api):
    """OpenAPI: Cart.products is an array of Product objects."""
    assert_schema(api.get("/carts/1").json(), "cart_spec")


@pytest.mark.smoke
@pytest.mark.negative
def test_FS_CARTS_011_get_nonexistent_cart_returns_4xx(api):
    assert_not_found(api.get("/carts/9999"))


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_012_get_cart_non_integer_id_returns_400(api):
    r = api.get("/carts/abc")
    assert r.status_code == 400, brief(r)
