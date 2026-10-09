"""ProofHub adapter (REST API v3, https://github.com/ProofHub/api_v3). Bugs = tasks in a task list."""
import html
import re

from .common import (DUPLICATE_THRESHOLD, Tracker, TrackerError, env_value, http_json, map_custom_fields,
                     similarity)


class ProofHub(Tracker):
    name = "proofhub"
    description_format = "html"

    def _base(self):
        if self.s.get("api_base"):  # override for local mock testing
            return self.s["api_base"].rstrip("/") + "/"
        company = (self.s.get("company") or "").strip()
        if not company or company == "yourcompany":
            raise TrackerError("Set proofhub.company (the subdomain of https://<company>.proofhub.com).")
        return f"https://{company}.proofhub.com/api/v3/"

    def _call(self, method, path, body=None):
        ua = (self.s.get("user_agent") or "").strip()
        if not ua:
            raise TrackerError("proofhub.user_agent is empty; ProofHub requires it, e.g. 'API-Testing-Skill (qa@company.com)'.")
        headers = {"X-API-KEY": env_value(self.s.get("api_key_env", "PROOFHUB_API_KEY"), "ProofHub API key"),
                   "User-Agent": ua}
        return http_json(method, self._base() + path.lstrip("/"), headers, body)

    @staticmethod
    def _list(data):
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            for k in ("data", "items", "results"):
                if isinstance(data.get(k), list):
                    return data[k]
        return []

    def config_problems(self):
        return [f"proofhub.{k} is not set" for k in ("project_id", "todolist_id") if not self.s.get(k)]

    def target(self):
        return f"ProofHub project {self.s.get('project_id')} -> task list {self.s.get('todolist_id')}"

    def build_payload(self, bug):
        labels = []
        sev = (self.s.get("severity_labels") or {}).get(bug["severity"])
        if sev:
            labels.append(int(sev))
        labels += [int(x) for x in (self.s.get("extra_labels") or []) if x]
        payload = {"title": self.title(bug), "description": self.description(bug),
                   "assigned": [int(x) for x in (self.s.get("default_assignees") or []) if x], "labels": labels}
        cf = map_custom_fields(self.s.get("custom_fields"), bug, wrap=lambda v: {"value": v})
        if cf:
            payload["custom_fields"] = cf
        return payload

    def preview_fields(self, p):
        rows = [("Title", p["title"]), ("Labels", p["labels"] or "(none - set proofhub.severity_labels)"),
                ("Assigned", p["assigned"] or "(nobody)")]
        if p.get("custom_fields"):
            rows.append(("Custom fields", p["custom_fields"]))
        return rows

    def preview_description(self, p):
        d = re.sub(r"<br>|</p>|</li>|</pre>", "\n", p["description"])
        d = re.sub(r"<li>", "  - ", d)
        return html.unescape(re.sub(r"<[^>]+>", "", d)).strip()

    def find_duplicates(self, title):
        _, data = self._call("GET", f"projects/{self.s['project_id']}/todolists/{self.s['todolist_id']}/tasks")
        hits = []
        for t in self._list(data):
            if t.get("completed"):
                continue
            sim = similarity(title, t.get("title", ""))
            if sim >= DUPLICATE_THRESHOLD:
                hits.append({"key": f"#{t.get('ticket') or t.get('id')}", "title": t.get("title"),
                             "url": self._url(t), "similarity": sim})
        return hits

    def _url(self, task):
        tpl = self.s.get("task_url_template") or ""
        return tpl.format(task_id=task.get("id", ""), ticket=task.get("ticket", ""),
                          project_id=self.s.get("project_id", ""), todolist_id=self.s.get("todolist_id", "")) if tpl else ""

    def create(self, payload):
        status, data = self._call("POST", f"projects/{self.s['project_id']}/todolists/{self.s['todolist_id']}/tasks", payload)
        if not isinstance(data, dict) or not data.get("id"):
            # ProofHub may answer 200 with {"code": 2033, "message": ...} for custom field mismatches
            raise TrackerError(f"ProofHub did not create the task (HTTP {status}): {str(data)[:400]}")
        return {"id": data["id"], "key": f"#{data.get('ticket') or data['id']}", "url": self._url(data)}

    def doctor(self):
        _, proj = self._call("GET", f"projects/{self.s['project_id']}")
        _, tasks = self._call("GET", f"projects/{self.s['project_id']}/todolists/{self.s['todolist_id']}/tasks")
        missing = [k for k, v in (self.s.get("severity_labels") or {}).items() if not v]
        lines = [f"Project: {(proj or {}).get('title') or (proj or {}).get('name')}",
                 f"Task list: reachable, {len(self._list(tasks))} tasks visible"]
        if missing:
            lines.append(f"Warning: no label ID for {missing}")
        return lines

    def lookups(self):
        def projects(a):
            return [(p.get("id"), p.get("title") or p.get("name")) for p in self._list(self._call("GET", "projects")[1])]

        def todolists(a):
            pid = a.project or self.s.get("project_id")
            if not pid:
                raise TrackerError("Pass --project ID")
            return [(t.get("id"), t.get("title") or t.get("name")) for t in self._list(self._call("GET", f"projects/{pid}/todolists")[1])]

        def labels(a):
            return [(x.get("id"), x.get("name")) for x in self._list(self._call("GET", "labels")[1])]

        def people(a):
            return [(p.get("id"), " ".join(filter(None, [p.get("first_name"), p.get("last_name")])) or p.get("email"))
                    for p in self._list(self._call("GET", "people")[1])]

        return {"projects": ("list projects -> project_id", projects),
                "todolists": ("task lists of --project -> todolist_id", todolists),
                "labels": ("labels -> severity_labels", labels),
                "people": ("people -> default_assignees", people)}
