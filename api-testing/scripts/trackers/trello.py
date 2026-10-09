"""Trello adapter (REST API v1). Bugs = cards in a list. Auth via Authorization header (keeps secrets out of URLs)."""
import urllib.parse

from .common import DUPLICATE_THRESHOLD, Tracker, TrackerError, env_value, http_json, similarity

API = "https://api.trello.com/1"


class Trello(Tracker):
    name = "trello"
    description_format = "markdown"

    def _call(self, method, path, body=None, params=None):
        key = env_value(self.s.get("api_key_env", "TRELLO_API_KEY"), "Trello API key")
        token = env_value(self.s.get("token_env", "TRELLO_TOKEN"), "Trello token")
        headers = {"Authorization": f'OAuth oauth_consumer_key="{key}", oauth_token="{token}"'}
        base = (self.s.get("api_base") or API).rstrip("/")
        url = base + path + ("?" + urllib.parse.urlencode(params) if params else "")
        return http_json(method, url, headers, body)

    def config_problems(self):
        return ["trello.list_id is not set"] if not self.s.get("list_id") else []

    def target(self):
        return f"Trello board {self.s.get('board_id') or '?'} -> list {self.s.get('list_id')}"

    def build_payload(self, bug):
        labels = []
        sev = (self.s.get("severity_labels") or {}).get(bug["severity"])
        if sev:
            labels.append(str(sev))
        labels += [str(x) for x in (self.s.get("extra_labels") or []) if x]
        return {"idList": self.s["list_id"], "name": self.title(bug), "desc": self.description(bug)[:16000],
                "idLabels": labels, "idMembers": [str(m) for m in (self.s.get("default_members") or []) if m],
                "pos": self.s.get("position") or "top"}

    def preview_fields(self, p):
        return [("Card title", p["name"]), ("Labels", p["idLabels"] or "(none - set trello.severity_labels)"),
                ("Members", p["idMembers"] or "(nobody)"), ("Position", p["pos"])]

    def preview_description(self, p):
        return p["desc"]

    def find_duplicates(self, title):
        if self.s.get("board_id"):
            _, cards = self._call("GET", f"/boards/{self.s['board_id']}/cards/open", params={"fields": "name,shortUrl"})
        else:
            _, cards = self._call("GET", f"/lists/{self.s['list_id']}/cards", params={"fields": "name,shortUrl,closed"})
        hits = []
        for c in cards or []:
            if c.get("closed"):
                continue
            sim = similarity(title, c.get("name", ""))
            if sim >= DUPLICATE_THRESHOLD:
                hits.append({"key": c.get("shortUrl", c.get("id")), "title": c.get("name"),
                             "url": c.get("shortUrl", ""), "similarity": sim})
        return hits

    def create(self, payload):
        _, data = self._call("POST", "/cards", payload)
        if not isinstance(data, dict) or not data.get("id"):
            raise TrackerError(f"Trello did not create the card: {str(data)[:400]}")
        return {"id": data["id"], "key": f"card {data.get('idShort', '')}".strip(), "url": data.get("shortUrl", "")}

    def doctor(self):
        _, me = self._call("GET", "/members/me", params={"fields": "username,fullName"})
        _, lst = self._call("GET", f"/lists/{self.s['list_id']}", params={"fields": "name,closed"})
        if (lst or {}).get("closed"):
            raise TrackerError("The configured Trello list is archived.")
        return [f"Logged in as: {(me or {}).get('fullName')} (@{(me or {}).get('username')})",
                f"List: {(lst or {}).get('name')}"]

    def lookups(self):
        def board_id(a):
            b = a.board or self.s.get("board_id")
            if not b:
                raise TrackerError("Pass --board ID (run: lookup boards)")
            return b

        def boards(a):
            return [(b.get("id"), b.get("name")) for b in
                    self._call("GET", "/members/me/boards", params={"fields": "name", "filter": "open"})[1] or []]

        def lists(a):
            return [(x.get("id"), x.get("name")) for x in self._call("GET", f"/boards/{board_id(a)}/lists")[1] or []]

        def labels(a):
            return [(x.get("id"), f"{x.get('name') or '(no name)'} [{x.get('color')}]")
                    for x in self._call("GET", f"/boards/{board_id(a)}/labels")[1] or []]

        def members(a):
            return [(m.get("id"), f"{m.get('fullName')} (@{m.get('username')})")
                    for m in self._call("GET", f"/boards/{board_id(a)}/members")[1] or []]

        return {"boards": ("your open boards -> board_id", boards),
                "lists": ("lists of --board -> list_id", lists),
                "labels": ("labels of --board -> severity_labels", labels),
                "members": ("members of --board -> default_members", members)}
