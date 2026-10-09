"""Cross-module data integrity: carts point to real products and real users; list and detail agree."""
import pytest


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_002_every_cart_product_exists_in_catalogue(api):
    product_ids = {p["id"] for p in api.get("/products").json()}
    missing = sorted({item.get("productId") for c in api.get("/carts").json()
                      for item in c.get("products", [])} - product_ids)
    assert not missing, f"carts reference product ids that are not in GET /products: {missing}"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_003_every_cart_belongs_to_an_existing_user(api):
    user_ids = {u["id"] for u in api.get("/users").json()}
    orphans = sorted({c["id"] for c in api.get("/carts").json() if c.get("userId") not in user_ids})
    assert not orphans, f"carts whose userId is not in GET /users: {orphans}"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_004_product_list_and_detail_return_same_data(api):
    for listed in api.get("/products", params={"limit": 5}).json():
        detail = api.get(f"/products/{listed['id']}").json()
        assert detail == listed, f"product {listed['id']}: list and detail differ"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_006_user_list_and_detail_return_same_data(api):
    for listed in api.get("/users").json()[:5]:
        detail = api.get(f"/users/{listed['id']}").json()
        assert detail == listed, f"user {listed['id']}: list and detail differ"


@pytest.mark.regression
@pytest.mark.positive
def test_FS_INTEG_007_cart_list_and_detail_return_same_data(api):
    for listed in api.get("/carts").json()[:5]:
        detail = api.get(f"/carts/{listed['id']}").json()
        assert detail == listed, f"cart {listed['id']}: list and detail differ"
