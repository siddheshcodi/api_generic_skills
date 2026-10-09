#!/usr/bin/env python3
"""
Build an endpoint inventory from an OpenAPI 3.x / Swagger 2.0 spec or a Postman v2.1 collection.

Usage:
  python api_inventory.py <spec.yaml|spec.json|collection.json|https://.../openapi.json> [--out DIR]

Writes DIR/endpoints.md (human table) and DIR/endpoints.json (for Claude), default DIR=./inventory.
Standard library only; PyYAML needed for YAML specs (pip install pyyaml).
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

METHODS = ["get", "post", "put", "patch", "delete", "head", "options"]


def load(source):
    if source.startswith(("http://", "https://")):
        with urllib.request.urlopen(source, timeout=30) as r:
            text = r.read().decode("utf-8")
    else:
        text = Path(source).read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml  # type: ignore
        except ImportError:
            sys.exit("ERROR: YAML spec needs PyYAML. Run: pip install pyyaml")
        return yaml.safe_load(text)


def resolve(doc, node, depth=0):
    """Resolve a local $ref (one level deep is enough for listing field names)."""
    if isinstance(node, dict) and "$ref" in node and depth < 5:
        ref = node["$ref"]
        if ref.startswith("#/"):
            target = doc
            for part in ref[2:].split("/"):
                target = target.get(part, {}) if isinstance(target, dict) else {}
            return resolve(doc, target, depth + 1)
    return node or {}


def schema_fields(doc, schema):
    schema = resolve(doc, schema)
    if schema.get("type") == "array":
        inner = schema_fields(doc, schema.get("items", {}))
        return f"array of {{{inner}}}" if inner else "array"
    for key in ("allOf", "oneOf", "anyOf"):
        if key in schema:
            parts = [schema_fields(doc, s) for s in schema[key]]
            return f" {key} ".join(p for p in parts if p)
    props = schema.get("properties") or {}
    req = set(schema.get("required") or [])
    return ", ".join(f"{n}{'*' if n in req else ''}:{resolve(doc, p).get('type', 'object')}" for n, p in props.items())


def ref_name(schema):
    if isinstance(schema, dict):
        if "$ref" in schema:
            return schema["$ref"].split("/")[-1]
        if schema.get("type") == "array" and isinstance(schema.get("items"), dict) and "$ref" in schema["items"]:
            return schema["items"]["$ref"].split("/")[-1] + "[]"
    return ""


def from_openapi(doc):
    is_v2 = "swagger" in doc
    global_sec = doc.get("security")
    if is_v2:
        base = (doc.get("schemes") or ["https"])[0] + "://" + doc.get("host", "") + doc.get("basePath", "")
        servers = [base]
    else:
        servers = [s.get("url") for s in doc.get("servers", [])]
    endpoints = []
    for path, item in (doc.get("paths") or {}).items():
        item = resolve(doc, item)
        shared = item.get("parameters", [])
        for m in METHODS:
            op = item.get(m)
            if not op:
                continue
            params = [resolve(doc, p) for p in shared + op.get("parameters", [])]
            body_fields, body_ref, content_type = "", "", ""
            if is_v2:
                for p in params:
                    if p.get("in") == "body":
                        body_fields, body_ref = schema_fields(doc, p.get("schema", {})), ref_name(p.get("schema", {}))
                params = [p for p in params if p.get("in") != "body"]
                content_type = ", ".join(op.get("consumes", doc.get("consumes", [])))
            else:
                rb = resolve(doc, op.get("requestBody", {}))
                content = rb.get("content", {})
                if content:
                    content_type = ", ".join(content.keys())
                    first = next(iter(content.values()))
                    body_fields, body_ref = schema_fields(doc, first.get("schema", {})), ref_name(first.get("schema", {}))
                    if rb.get("required"):
                        body_fields = "(required) " + body_fields
            responses = {}
            for code, r in (op.get("responses") or {}).items():
                r = resolve(doc, r)
                schema = r.get("schema") if is_v2 else next(iter((r.get("content") or {}).values()), {}).get("schema")
                responses[str(code)] = ref_name(schema or {}) or r.get("description", "")[:60]
            security = op.get("security", global_sec)
            auth = "none" if security == [] else (", ".join(k for s in (security or []) for k in s) or "unspecified")
            endpoints.append({
                "method": m.upper(), "path": path,
                "summary": op.get("summary") or op.get("operationId") or "",
                "tags": op.get("tags", []), "deprecated": bool(op.get("deprecated")),
                "auth": auth,
                "path_params": [f"{p['name']}{'*' if p.get('required') else ''}" for p in params if p.get("in") == "path"],
                "query_params": [f"{p['name']}{'*' if p.get('required') else ''}" for p in params if p.get("in") == "query"],
                "header_params": [f"{p['name']}{'*' if p.get('required') else ''}" for p in params if p.get("in") == "header"],
                "content_type": content_type, "body_schema": body_ref, "body_fields": body_fields,
                "responses": responses,
            })
    schemes = doc.get("securityDefinitions") if is_v2 else (doc.get("components") or {}).get("securitySchemes")
    info = doc.get("info", {})
    return {"source_type": "swagger2" if is_v2 else "openapi3", "title": info.get("title"),
            "version": info.get("version"), "servers": servers, "security_schemes": schemes or {},
            "endpoints": endpoints}


def from_postman(doc):
    endpoints = []

    def walk(items, folder):
        for it in items:
            if "item" in it:
                walk(it["item"], folder + [it.get("name", "")])
                continue
            req = it.get("request") or {}
            if isinstance(req, str):
                req = {"url": req, "method": "GET"}
            url = req.get("url", "")
            if isinstance(url, dict):
                path = "/" + "/".join(url.get("path", [])) if url.get("path") else url.get("raw", "")
                query = [q.get("key") for q in url.get("query", []) if not q.get("disabled")]
                raw = url.get("raw", "")
            else:
                raw, query = url, []
                path = re.sub(r"^\{\{[^}]+\}\}", "", url.split("?")[0]) or url
            body = req.get("body") or {}
            body_fields = ""
            if body.get("mode") == "raw":
                try:
                    parsed = json.loads(body.get("raw") or "{}")
                    body_fields = ", ".join(parsed.keys()) if isinstance(parsed, dict) else "json array"
                except json.JSONDecodeError:
                    body_fields = "raw (non-JSON or uses variables)"
            elif body.get("mode") in ("formdata", "urlencoded"):
                body_fields = ", ".join(f.get("key", "") for f in body.get(body["mode"], []))
            auth = (req.get("auth") or {}).get("type") or "inherited"
            tests = [e for e in it.get("event", []) if e.get("listen") == "test"]
            endpoints.append({
                "method": req.get("method", "GET"), "path": path, "raw_url": raw,
                "summary": it.get("name", ""), "tags": [f for f in folder if f], "deprecated": False,
                "auth": auth, "path_params": [], "query_params": query, "header_params":
                [h.get("key") for h in req.get("header", []) if not h.get("disabled")],
                "content_type": body.get("mode", ""), "body_schema": "", "body_fields": body_fields,
                "responses": {str(r.get("code")): r.get("name", "") for r in it.get("response", [])},
                "has_postman_tests": bool(tests),
            })

    walk(doc.get("item", []), [])
    info = doc.get("info", {})
    return {"source_type": "postman", "title": info.get("name"), "version": info.get("version"),
            "servers": [v.get("value") for v in doc.get("variable", []) if "url" in (v.get("key") or "").lower()],
            "security_schemes": (doc.get("auth") or {}).get("type", ""), "endpoints": endpoints}


def to_markdown(inv):
    lines = [f"# Endpoint inventory — {inv.get('title') or 'API'} {inv.get('version') or ''}".rstrip(), "",
             f"Source type: {inv['source_type']} · Servers: {', '.join(filter(None, inv['servers'])) or 'n/a'} · "
             f"Endpoints: {len(inv['endpoints'])}", "",
             "`*` = required. Body/response names are schema names from the spec.", "",
             "| # | Method | Path | Summary | Tags | Auth | Path params | Query params | Body | Responses |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for i, e in enumerate(inv["endpoints"], 1):
        body = e["body_schema"] or e["body_fields"]
        if e["body_schema"] and e["body_fields"]:
            body = f"{e['body_schema']} ({e['body_fields']})"
        resp = ", ".join(f"{k}:{v}" if v else k for k, v in e["responses"].items())
        summary = e["summary"] + (" (deprecated)" if e["deprecated"] else "")
        cells = [str(i), e["method"], f"`{e['path']}`", summary, ", ".join(e["tags"]), e["auth"],
                 ", ".join(e["path_params"]), ", ".join(e["query_params"]), body, resp]
        lines.append("| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |")
    no_errors = [f"{e['method']} {e['path']}" for e in inv["endpoints"]
                 if not any(c.startswith(("4", "5")) for c in e["responses"])]
    if no_errors:
        lines += ["", "## Endpoints with no documented error responses (ask what they should return)"]
        lines += [f"- {x}" for x in no_errors]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("--out", default="inventory")
    args = ap.parse_args()

    doc = load(args.source)
    if not isinstance(doc, dict):
        sys.exit("ERROR: file is not a JSON/YAML object")
    if "openapi" in doc or "swagger" in doc:
        inv = from_openapi(doc)
    elif "item" in doc and "info" in doc:
        inv = from_postman(doc)
    else:
        sys.exit("ERROR: not recognised as OpenAPI/Swagger or Postman v2.x collection")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "endpoints.json").write_text(json.dumps(inv, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "endpoints.md").write_text(to_markdown(inv), encoding="utf-8")
    by_method = {}
    for e in inv["endpoints"]:
        by_method[e["method"]] = by_method.get(e["method"], 0) + 1
    print(f"{inv['source_type']}: {len(inv['endpoints'])} endpoints {by_method} -> {out}/endpoints.md, endpoints.json")


if __name__ == "__main__":
    main()
