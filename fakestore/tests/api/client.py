import time
import requests


class ApiClient:
    """Small wrapper: base URL, default headers, timeout, timing, rate-limit wait.

    Uses a fresh request per call (no cookie jar): if an API sets auth cookies on login, a
    shared session would silently authenticate the "no token" tests.
    """

    def __init__(self, base_url, headers=None, timeout=30, max_retries=3):
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})
        self.timeout = timeout
        self.max_retries = max_retries

    def request(self, method, path, headers=None, **kwargs):
        kwargs.setdefault("timeout", self.timeout)
        hdrs = {**self.headers, **(headers or {})}
        for attempt in range(self.max_retries + 1):
            start = time.perf_counter()
            resp = requests.request(method, f"{self.base_url}{path}", headers=hdrs, **kwargs)
            resp.elapsed_ms = round((time.perf_counter() - start) * 1000)
            if resp.status_code != 429 or attempt == self.max_retries:
                return resp
            # rate limited (100 requests / window): wait for the window to reset, then retry
            wait = resp.headers.get("retry-after")
            reset = resp.headers.get("x-ratelimit-reset")
            if wait and wait.isdigit():
                delay = int(wait)
            elif reset and reset.isdigit():
                delay = max(1, int(reset) - int(time.time()))
            else:
                delay = 5
            time.sleep(min(delay, 60))
        return resp

    def get(self, path, **kw):    return self.request("GET", path, **kw)
    def post(self, path, **kw):   return self.request("POST", path, **kw)
    def put(self, path, **kw):    return self.request("PUT", path, **kw)
    def patch(self, path, **kw):  return self.request("PATCH", path, **kw)
    def delete(self, path, **kw): return self.request("DELETE", path, **kw)
