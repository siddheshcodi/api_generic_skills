"""Read-only consistency between modules (writes are not persisted, so flows use stored data)."""
from urllib.parse import quote

import pytest


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_INTEGRATION_003_every_cart_product_exists(api):
    product_ids = {p["id"] for p in api.get("/products").json()}
    for cart in api.get("/carts").json():
        missing = [i["productId"] for i in cart["products"] if i["productId"] not in product_ids]
        assert not missing, f"cart {cart['id']} references unknown products {missing}"


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_INTEGRATION_004_every_cart_owner_exists(api):
    user_ids = {u["id"] for u in api.get("/users").json()}
    orphans = {c["id"]: c["userId"] for c in api.get("/carts").json() if c["userId"] not in user_ids}
    assert not orphans, f"carts with unknown owners: {orphans}"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_005_carts_by_user_match_full_cart_list(api):
    all_carts = api.get("/carts").json()
    for uid in sorted({c["userId"] for c in all_carts}):
        expected = sorted(c["id"] for c in all_carts if c["userId"] == uid)
        got = sorted(c["id"] for c in api.get(f"/carts/user/{uid}").json())
        assert got == expected, f"user {uid}: /carts/user -> {got}, /carts -> {expected}"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_006_category_list_matches_product_categories(api):
    used = {p["category"] for p in api.get("/products").json()}
    assert set(api.get("/products/categories").json()) == used


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_007_category_endpoint_matches_product_list(api):
    products = api.get("/products").json()
    for cat in api.get("/products/categories").json():
        expected = sorted(p["id"] for p in products if p["category"] == cat)
        got = sorted(p["id"] for p in api.get(f"/products/category/{quote(cat)}").json())
        assert got == expected, f"category {cat!r}: endpoint {got} vs list {expected}"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_008_product_detail_matches_list_entry(api):
    listed = {p["id"]: p for p in api.get("/products").json()}
    for pid in (1, 10, 20):
        assert api.get(f"/products/{pid}").json() == listed[pid], f"product {pid} differs between list and detail"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_009_user_detail_matches_list_entry(api):
    listed = {u["id"]: u for u in api.get("/users").json()}
    for uid in (1, 5, 10):
        assert api.get(f"/users/{uid}").json() == listed[uid], f"user {uid} differs between list and detail"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEGRATION_010_cart_value_can_be_priced_from_catalogue(api):
    prices = {p["id"]: p["price"] for p in api.get("/products").json()}
    cart = api.get("/carts/1").json()
    total = round(sum(prices[i["productId"]] * i["quantity"] for i in cart["products"]), 2)
    assert total > 0 and all(i["quantity"] > 0 for i in cart["products"]), f"cart 1 total {total}"
