"""Shared helpers for bug tracker adapters: errors, HTTP, secret masking, description rendering."""
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SEVERITIES = ["Critical", "High", "Medium", "Low"]


class TrackerError(Exception):
    """Raised for any problem the user must fix (config, auth, network, API error)."""


def die(msg, code=1):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def env_value(name, what):
    if not name:
        raise TrackerError(f"Config is missing the environment variable name for {what}.")
    value = os.getenv(name)
    if not value:
        raise TrackerError(f"Environment variable {name} ({what}) is not set. Set it in your terminal, "
                           f"never in the config file.")
    return value


# ----------------------------------------------------------------------------- HTTP
HTTP_HINTS = {
    400: "request rejected - check required fields / config values",
    401: "authentication failed - check the API key/token env vars",
    403: "no permission for this project/board/list",
    404: "not found - check IDs/keys/base URL in config",
    410: "endpoint removed by the vendor - update the adapter",
    415: "content type problem",
}


def http_json(method, url, headers=None, body=None, retry=True, timeout=30):
    headers = dict(headers or {})
    headers.setdefault("Accept", "application/json")
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, (json.loads(raw) if raw.strip() else None)
    except urllib.error.HTTPError as e:
        if e.code == 429 and retry:
            wait = min(int(e.headers.get("Retry-After", "10") or 10), 60)
            print(f"Rate limited, waiting {wait}s and retrying once...", file=sys.stderr)
            time.sleep(wait)
            return http_json(method, url, headers, body, retry=False, timeout=timeout)
        detail = mask(e.read().decode("utf-8", "replace")[:600])
        safe_url = url.split("?")[0]
        raise TrackerError(f"HTTP {e.code} on {method} {safe_url}: {detail} "
                           f"({HTTP_HINTS.get(e.code, 'see the tracker reference file')})")
    except urllib.error.URLError as e:
        raise TrackerError(f"Cannot reach {urllib.parse.urlsplit(url).netloc} ({e.reason}). If you are in a "
                           f"sandbox (e.g. the Claude chat app), run this command on your own machine.")


# ----------------------------------------------------------------------------- masking
_MASKS = [
    (re.compile(r"(?i)(authorization\s*[:=]\s*(?:bearer|basic|token|oauth)\s+)(?!<)[^\s'\"]{6,}"), r"\1<MASKED>"),
    (re.compile(r"(?i)(authorization\s*[:=]\s*)(?!(?:bearer|basic|token|oauth)\b)(?!<)[^\s'\"]{6,}"), r"\1<MASKED>"),
    (re.compile(r"(?i)\b(bearer\s+)(?!<)[A-Za-z0-9._\-+/=]{10,}"), r"\1<MASKED>"),
    (re.compile(r'(?i)("?(?:password|passwd|pwd|secret|client_secret|api[_-]?key|access_token|refresh_token|token)"?\s*[:=]\s*)"[^"<]{3,}"'), r'\1"<MASKED>"'),
    (re.compile(r"(?i)((?:password|secret|api[_-]?key|access_token|token|key)=)[^&\s'\"<]{3,}"), r"\1<MASKED>"),
    (re.compile(r"(?i)(x-api-key\s*:\s*)[^'\"\s]{6,}"), r"\1<MASKED>"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\b"), "<MASKED_JWT>"),
]


def mask(text):
    if text is None:
        return ""
    text = str(text)
    for pattern, repl in _MASKS:
        text = pattern.sub(repl, text)
    return text


# ----------------------------------------------------------------------------- duplicates
def norm_title(title):
    t = re.sub(r"^\s*(\[[^\]]*\]\s*)+", "", title or "")
    return re.sub(r"\s+", " ", t).strip().lower()


def similarity(a, b):
    return round(difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio(), 2)


DUPLICATE_THRESHOLD = 0.85


# ----------------------------------------------------------------------------- description
def _fmt(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False)
    return "" if value is None else str(value)


def bug_sections(bug):
    """Tracker-neutral description: list of (kind, heading, content). Everything is masked here."""
    resp = bug.get("response") or {}
    req = bug.get("request") or {}
    facts = [
        ("Bug ID", bug.get("bug_id")), ("Severity", bug.get("severity")), ("Priority", bug.get("priority")),
        ("Environment", f"{bug.get('environment', '')} {bug.get('base_url', '')}".strip()),
        ("Endpoint", f"{bug['method']} {bug['endpoint']}"), ("Test case", bug.get("test_case_id")),
        ("Category", bug.get("category")), ("Reproducibility", bug.get("reproducibility")),
        ("Found at", bug.get("found_at")),
    ]
    out = [("text", "Description (in simple words)", mask(bug["description"])),
           ("facts", "", [(k, mask(v)) for k, v in facts if v])]
    if bug.get("preconditions"):
        out.append(("text", "Preconditions", mask(bug["preconditions"])))
    if bug.get("steps"):
        out.append(("steps", "Steps to reproduce", [mask(s) for s in bug["steps"]]))
    if req.get("curl"):
        out.append(("code", "Request (cURL)", mask(req["curl"])))
    out.append(("text", "Expected", mask(bug["expected"])))
    out.append(("text", "Actual", mask(bug["actual"])))
    if resp:
        out.append(("text", "Response", f"Status {resp.get('status', '?')}, {resp.get('time_ms', '?')} ms"))
        if resp.get("headers"):
            out.append(("code", "Response headers", mask(_fmt(resp["headers"]))))
        if resp.get("body"):
            out.append(("code", "Response body", mask(_fmt(resp["body"]))[:3000]))
    if bug.get("affected_endpoints"):
        out.append(("list", "Also affects", [mask(a) for a in bug["affected_endpoints"]]))
    if bug.get("notes"):
        out.append(("text", "Notes", mask(bug["notes"])))
    out.append(("footer", "", "Reported via api-testing skill (reviewed and approved by QA before creation)."))
    return out


def _wiki_escape(text):
    """Stop Jira wiki markup from treating {...} [..] |  as macros/links/tables in plain text."""
    return re.sub(r"([{}\[\]|])", r"\\\1", str(text))


def render(sections, fmt):
    """fmt: html | markdown | jira_wiki | text"""
    lines = []
    for kind, head, content in sections:
        if fmt == "html":
            e = html.escape
            if kind == "facts":
                lines.append("<p>" + "<br>".join(f"<b>{e(k)}:</b> {e(str(v))}" for k, v in content) + "</p>")
            elif kind == "text":
                lines.append(f"<p><b>{e(head)}</b><br>{e(content)}</p>")
            elif kind == "code":
                lines.append(f"<p><b>{e(head)}</b></p><pre>{e(content)}</pre>")
            elif kind == "steps":
                lines.append(f"<p><b>{e(head)}</b></p><ol>" + "".join(f"<li>{e(s)}</li>" for s in content) + "</ol>")
            elif kind == "list":
                lines.append(f"<p><b>{e(head)}</b></p><ul>" + "".join(f"<li>{e(s)}</li>" for s in content) + "</ul>")
            elif kind == "footer":
                lines.append(f"<p><i>{e(content)}</i></p>")
        elif fmt == "jira_wiki":
            w = _wiki_escape
            if kind == "facts":
                lines += [f"*{k}:* {w(v)}" for k, v in content]
            elif kind == "text":
                lines += ["", f"h4. {head}", w(content)]
            elif kind == "code":
                lines += ["", f"h4. {head}", "{noformat}", content, "{noformat}"]
            elif kind == "steps":
                lines += ["", f"h4. {head}"] + [f"# {w(s)}" for s in content]
            elif kind == "list":
                lines += ["", f"h4. {head}"] + [f"* {w(s)}" for s in content]
            elif kind == "footer":
                lines += ["", f"_{content}_"]
        elif fmt == "markdown":
            if kind == "facts":
                lines += [""] + [f"**{k}:** {v}  " for k, v in content]
            elif kind == "text":
                lines += ["", f"**{head}**", "", content]
            elif kind == "code":
                lines += ["", f"**{head}**", "", "```", content, "```"]
            elif kind == "steps":
                lines += ["", f"**{head}**", ""] + [f"{i}. {s}" for i, s in enumerate(content, 1)]
            elif kind == "list":
                lines += ["", f"**{head}**", ""] + [f"- {s}" for s in content]
            elif kind == "footer":
                lines += ["", f"_{content}_"]
        else:  # text
            if kind == "facts":
                lines += [""] + [f"{k}: {v}" for k, v in content]
            elif kind in ("text", "code"):
                lines += ["", f"{head}:", content]
            elif kind == "steps":
                lines += ["", f"{head}:"] + [f"{i}. {s}" for i, s in enumerate(content, 1)]
            elif kind == "list":
                lines += ["", f"{head}:"] + [f"- {s}" for s in content]
            elif kind == "footer":
                lines += ["", content]
    return ("" if fmt == "html" else "\n").join(lines)


def full_title(prefix, bug):
    title = mask(bug["title"]).strip()
    prefix = (prefix or "").strip()
    return f"{prefix} [{bug['severity']}] {title}".strip()


# ----------------------------------------------------------------------------- adapter base
class Tracker:
    """Interface every adapter implements. See references/trackers/adding-a-tracker.md."""

    name = "base"
    description_format = "text"

    def __init__(self, settings, common):
        self.s = settings or {}
        self.common = common  # dict with title_prefix, reports_dir, config_dir

    # --- static checks (no network)
    def config_problems(self):
        return []

    def target(self):
        """Human-readable 'where the bug will go'."""
        return self.name

    # --- payload
    def title(self, bug):
        return full_title(self.common.get("title_prefix"), bug)

    def description(self, bug):
        return render(bug_sections(bug), self.s.get("description_format") or self.description_format)

    def build_payload(self, bug):
        raise NotImplementedError

    def preview_fields(self, payload):
        """[(label, value)] shown above the description in previews."""
        return []

    def preview_description(self, payload):
        return ""

    # --- network
    def find_duplicates(self, title):
        """[{key, title, url, similarity}] of OPEN items similar to title."""
        return []

    def create(self, payload):
        """Return {id, key, url}."""
        raise NotImplementedError

    def doctor(self):
        """Return list of 'label: value' lines; raise TrackerError on failure."""
        return []

    def lookups(self):
        """{name: (help, callable(args) -> [(id, label)])}"""
        return {}


def map_custom_fields(rules, bug, wrap=None):
    """rules: {field_id: {from: bug_key, values: {bug_value: tracker_value}}} -> {field_id: value}"""
    out = {}
    for field_id, rule in (rules or {}).items():
        rule = rule or {}
        value = bug.get(rule.get("from", ""))
        if value in (None, ""):
            continue
        mapped = (rule.get("values") or {}).get(value, value)
        out[str(field_id)] = wrap(mapped) if wrap else mapped
    return out
