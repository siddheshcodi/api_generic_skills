from urllib.parse import quote

import pytest

from helpers import brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_PRODUCTS_010_list_categories(api):
    r = api.get("/products/categories")
    assert r.status_code == 200, brief(r)
    cats = r.json()
    assert len(cats) == 4 and all(isinstance(c, str) and c for c in cats), cats


@pytest.mark.regression
@pytest.mark.positive
@pytest.mark.parametrize("category", ["electronics", "men's clothing"])
def test_FS_PRODUCTS_011_products_in_category_belong_to_it(api, category):
    products = api.get(f"/products/category/{quote(category)}").json()
    assert products and {p["category"] for p in products} == {category}


@pytest.mark.regression
@pytest.mark.negative
def test_FS_PRODUCTS_012_unknown_category_returns_empty_list(api):
    r = api.get("/products/category/qa_auto_no_such_category")
    assert r.status_code == 200, brief(r)
    assert r.json() == []
