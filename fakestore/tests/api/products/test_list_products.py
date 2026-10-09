import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_PRODUCTS_001_list_all_products(api):
    r = api.get("/products")
    assert r.status_code == 200, brief(r)
    products = r.json()
    assert isinstance(products, list) and len(products) == 20
    for p in products:
        assert_schema(p, "product")


@pytest.mark.regression
@pytest.mark.positive
def test_FS_PRODUCTS_002_limit_returns_that_many_products(api):
    products = api.get("/products?limit=5").json()
    assert [p["id"] for p in products] == [1, 2, 3, 4, 5]


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize("order", ["asc", "desc"])
def test_FS_PRODUCTS_003_sort_orders_products_by_id(api, order):
    ids = [p["id"] for p in api.get(f"/products?sort={order}").json()]
    assert ids == sorted(ids, reverse=order == "desc"), ids


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize("query", ["limit=-1", "limit=abc", "sort=sideways"], ids=["negative_limit", "text_limit", "bad_sort"])
def test_FS_PRODUCTS_004_invalid_list_params_never_break_the_list(api, query):
    """limit/sort are not in the spec: invalid values must not cause 5xx or a broken body."""
    r = api.get(f"/products?{query}")
    assert r.status_code in (200, 400), brief(r)
    if r.status_code == 200:
        assert isinstance(r.json(), list) and r.json(), "expected the normal product list"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_PRODUCTS_005_list_responds_within_sla(api, config):
    r = api.get("/products")
    limit = config["defaults"]["max_response_time_ms"]
    assert r.elapsed_ms <= limit, f"GET /products took {r.elapsed_ms} ms (limit {limit} ms)"
