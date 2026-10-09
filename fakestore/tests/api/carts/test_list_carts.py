import pytest

from helpers import assert_schema, brief


@pytest.mark.smoke
@pytest.mark.positive
def test_FS_CARTS_001_list_all_carts(api):
    r = api.get("/carts")
    assert r.status_code == 200, brief(r)
    carts = r.json()
    assert carts
    for c in carts:
        assert_schema(c, "cart")


@pytest.mark.regression
@pytest.mark.positive
def test_FS_CARTS_002_limit_and_sort_carts(api):
    carts = api.get("/carts?limit=2&sort=desc").json()
    ids = [c["id"] for c in carts]
    assert len(ids) == 2 and ids == sorted(ids, reverse=True), ids


@pytest.mark.regression
@pytest.mark.positive
def test_FS_CARTS_003_date_range_returns_only_carts_in_range(api):
    carts = api.get("/carts?startdate=2020-01-01&enddate=2020-03-01").json()
    assert carts
    for c in carts:
        assert "2020-01-01" <= c["date"][:10] <= "2020-03-01", f"cart {c['id']} date {c['date']} outside range"


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_004_invalid_date_format_returns_400(api):
    r = api.get("/carts?startdate=notadate")
    assert r.status_code == 400, brief(r)
    assert "yyyy-mm-dd" in r.json().get("message", "")


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_005_reversed_date_range_returns_empty_list(api):
    r = api.get("/carts?startdate=2021-01-01&enddate=2019-01-01")
    assert r.status_code in (200, 400), brief(r)
    if r.status_code == 200:
        assert r.json() == []


@pytest.mark.regression
@pytest.mark.positive
def test_FS_CARTS_006_get_carts_of_a_user(api):
    carts = api.get("/carts/user/2").json()
    assert carts and all(c["userId"] == 2 for c in carts)


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_007_carts_of_unknown_user_is_empty_or_4xx(api):
    r = api.get("/carts/user/9999")
    assert r.status_code in (200, 400, 404), brief(r)
    if r.status_code == 200:
        assert r.json() == []


@pytest.mark.regression
@pytest.mark.negative
def test_FS_CARTS_008_carts_of_non_integer_user_returns_400(api):
    r = api.get("/carts/user/abc")
    assert r.status_code == 400, brief(r)
