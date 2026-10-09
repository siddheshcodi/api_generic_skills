import pytest

from helpers import assert_json_object, assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_CARTS_002_get_single_cart_matches_spec_schema(api):
    r = api.get("/carts/1")
    assert r.status_code == 200, brief(r)
    assert_json_object(r)
    assert_schema(r.json(), "cart")


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_003_get_nonexistent_cart_is_not_empty_200(api):
    r = api.get("/carts/9999")
    assert r.status_code in (400, 404), f"expected 400/404 for unknown id, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_008_get_cart_with_non_numeric_id_returns_400(api):
    r = api.get("/carts/abc")
    assert r.status_code == 400, brief(r)
