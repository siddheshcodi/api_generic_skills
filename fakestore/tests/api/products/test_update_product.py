import pytest

from helpers import assert_not_found, brief


@pytest.mark.smoke
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_018_update_product_with_put(api):
    r = api.put("/products/1", json={"title": "qa_auto new title", "price": 20})
    assert r.status_code == 200, brief(r)
    assert r.json()["id"] == 1 and r.json()["title"] == "qa_auto new title"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.positive
def test_FS_PRODUCTS_019_update_product_with_patch(api):
    r = api.patch("/products/1", json={"price": 1.25})
    assert r.status_code == 200, brief(r)
    assert r.json()["price"] == 1.25 and r.json()["id"] == 1


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_020_update_nonexistent_product_returns_4xx(api):
    assert_not_found(api.put("/products/9999", json={"title": "x"}))


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_021_update_product_non_integer_id_returns_400(api):
    r = api.put("/products/abc", json={"title": "x"})
    assert r.status_code == 400, brief(r)


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_022_update_product_with_text_price_returns_400(api):
    r = api.put("/products/1", json={"price": "abc"})
    assert r.status_code == 400, f"price 'abc' should be rejected, got {brief(r)}"


@pytest.mark.regression
@pytest.mark.destructive
@pytest.mark.negative
def test_FS_PRODUCTS_023_id_in_body_does_not_override_url_id(api):
    r = api.put("/products/1", json={"id": 777, "title": "qa_auto"})
    assert r.status_code in (200, 400), brief(r)
    if r.status_code == 200:
        assert r.json()["id"] == 1, f"URL says product 1, response id is {r.json()['id']}"
