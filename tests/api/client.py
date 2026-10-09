import time
import requests


class ApiClient:
    """Small wrapper: base URL, default headers, timeout, timing."""

    def __init__(self, base_url, headers=None, timeout=30):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.timeout = timeout

    def request(self, method, path, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        start = time.perf_counter()
        resp = self.session.request(method, f"{self.base_url}{path}", **kwargs)
        resp.elapsed_ms = round((time.perf_counter() - start) * 1000)
        return resp

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
