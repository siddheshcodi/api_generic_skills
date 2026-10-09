import pytest
import requests


@pytest.mark.regression
@pytest.mark.positive
def test_FS_PRODUCTS_028_plain_http_redirects_to_https(api):
    r = requests.get(api.base_url.replace("https://", "http://") + "/products/1", allow_redirects=False, timeout=30)
    assert r.status_code in (301, 308) and r.headers.get("location", "").startswith("https://"), r.status_code


@pytest.mark.regression
@pytest.mark.negative
def test_FS_PRODUCTS_029_response_does_not_reveal_server_framework(api):
    r = api.get("/products/1")
    assert "x-powered-by" not in {k.lower() for k in r.headers}, f"X-Powered-By: {r.headers.get('x-powered-by')}"
