import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_CARTS_025_delete_cart(api):
    r = api.delete("/carts/1")
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_026_delete_nonexistent_cart_returns_4xx(api):
    assert_not_found(api.delete("/carts/9999"))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_CARTS_027_delete_cart_non_integer_id_returns_400(api):
    r = api.delete("/carts/abc")
    assert r.status_code == 400, brief(r)
