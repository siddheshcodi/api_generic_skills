import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_PRODUCTS_001_list_all_products(api):
    r = api.get("/products")
    assert r.status_code == 200, brief(r)
    assert r.headers["Content-Type"].startswith("application/json")
    body = r.json()
    assert isinstance(body, list) and body, "expected a non-empty list"
    for p in body:
        assert_schema(p, "product")


@pytest.mark.regression
@pytest.mark.positive
def test_FS_PRODUCTS_002_limit_returns_that_many(api):
    r = api.get("/products", params={"limit": 5})
    assert r.status_code == 200, brief(r)
    assert len(r.json()) == 5


@pytest.mark.regression
@pytest.mark.positive
def test_FS_PRODUCTS_003_sort_desc_orders_by_id_descending(api):
    ids = [p["id"] for p in api.get("/products", params={"sort": "desc"}).json()]
    assert ids == sorted(ids, reverse=True), ids
