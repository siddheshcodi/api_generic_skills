#!/usr/bin/env python3
"""
Module-wise test plan and execution report: joins the designed test cases, the JUnit results
and the bug files into one report showing WHAT was tested (positive / negative per module),
what passed or failed, and which bug each failure belongs to.

Usage:
  python test_report.py --cases <reports_dir>/test-cases.json --plan-only --out <reports_dir>
      -> test-cases.md                      (Step 4: the plan, module-wise)
  python test_report.py --cases <reports_dir>/test-cases.json <junit.xml ...> \
                        [--bugs <reports_dir>/bugs] --out <reports_dir>
      -> test-cases.md, test-report.md, test-report.csv   (Step 9: plan + results + bugs)

test-cases.json format: see assets/test-cases.example.json. Test IDs are matched to JUnit results
the same way as parse_results.py (ID in the test name). Standard library only.
"""
import argparse
import csv
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from parse_results import collect, parse  # noqa: E402

TYPES = ("positive", "negative")
REQUIRED = ("id", "module", "endpoint", "title", "type", "expected")
ICON = {"passed": "✅ Pass", "failed": "❌ Fail", "error": "⚠️ Error", "skipped": "⏭ Skipped",
        "not run": "– Not run"}
SEV_ORDER = ["Critical", "High", "Medium", "Low"]


def die(msg):
    sys.exit(f"ERROR: {msg}")


def load_cases(path):
    try:
        doc = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        die(f"cannot read {path}: {e}")
    cases, problems, seen = doc.get("cases") or [], [], set()
    for i, c in enumerate(cases, 1):
        missing = [k for k in REQUIRED if not c.get(k)]
        if missing:
            problems.append(f"case #{i} ({c.get('id', '?')}): missing {missing}")
        if c.get("type") and c["type"] not in TYPES:
            problems.append(f"{c.get('id')}: type must be one of {TYPES}, got '{c['type']}'")
        if c.get("id") in seen:
            problems.append(f"duplicate id {c['id']}")
        seen.add(c.get("id"))
    if problems:
        die("test-cases.json problems:\n  " + "\n  ".join(problems))
    return doc, cases


def load_bugs(folder):
    bugs = []
    for p in sorted(Path(folder).glob("BUG-*.json")) if folder and Path(folder).is_dir() else []:
        try:
            b = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        ids = [b.get("test_case_id")] + list(b.get("test_case_ids") or [])
        b["_tests"] = list(OrderedDict.fromkeys(i for i in ids if i))
        bugs.append(b)
    return bugs


def results_by_id(junit_paths):
    """test_id -> aggregated status (parametrized runs: worst wins) + first failure message."""
    rank = {"error": 3, "failed": 2, "passed": 1, "skipped": 0}
    out, unplanned = {}, []
    for c in parse(collect(junit_paths)) if junit_paths else []:
        if not c["test_id"]:
            unplanned.append(c)
            continue
        cur = out.setdefault(c["test_id"], {"status": c["status"], "message": "", "runs": 0, "time_s": 0.0})
        cur["runs"] += 1
        cur["time_s"] += c["time_s"]
        if rank[c["status"]] > rank[cur["status"]]:
            cur["status"] = c["status"]
        if c["status"] in ("failed", "error") and not cur["message"]:
            msg = (c["message"] or c["details"]).split("\n")[0]
            cur["message"] = msg.replace("AssertionError: ", "")[:220]
    return out, unplanned


def cell(text):
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def pct(a, b):
    return f"{round(100 * a / b, 1)}%" if b else "–"


# ----------------------------------------------------------------------------- plan
def render_plan(doc, cases):
    mods = OrderedDict()
    for c in cases:
        mods.setdefault(c["module"], []).append(c)
    md = [f"# Test cases — {doc.get('project', 'API')}", "",
          f"Environment: {doc.get('environment', '')} · Source: {doc.get('source', '')} · "
          f"Author: {doc.get('author', '')} · Date: {doc.get('date', '')}", "",
          "## Coverage summary", "",
          "| Module | Endpoints | Positive | Negative | Total |", "|---|---|---|---|---|"]
    for m, cs in mods.items():
        eps = len({c["endpoint"] for c in cs})
        pos = sum(c["type"] == "positive" for c in cs)
        md.append(f"| {m} | {eps} | {pos} | {len(cs) - pos} | {len(cs)} |")
    pos = sum(c["type"] == "positive" for c in cases)
    md.append(f"| **All** | **{len({c['endpoint'] for c in cases})}** | **{pos}** | **{len(cases) - pos}** | **{len(cases)}** |")
    for m, cs in mods.items():
        md += ["", f"## {m}"]
        if (doc.get("modules") or {}).get(m):
            md += ["", doc["modules"][m]]
        md += ["", "Endpoints: " + ", ".join(f"`{e}`" for e in OrderedDict.fromkeys(c["endpoint"] for c in cs))]
        for t in TYPES:
            group = [c for c in cs if c["type"] == t]
            if not group:
                continue
            md += ["", f"### {t.capitalize()} scenarios ({len(group)})", "",
                   "| ID | Scenario | Endpoint | Category | Priority | Request / data | Expected result |",
                   "|---|---|---|---|---|---|---|"]
            md += [f"| {c['id']} | {cell(c['title'])} | `{cell(c['endpoint'])}` | {cell(c.get('category'))} | "
                   f"{cell(c.get('priority'))} | {cell(c.get('request'))} | {cell(c['expected'])} |" for c in group]
    if doc.get("assumptions"):
        md += ["", "## Assumptions and open questions", ""] + [f"- {a}" for a in doc["assumptions"]]
    return "\n".join(md) + "\n"


# ----------------------------------------------------------------------------- report
def render_report(doc, cases, res, unplanned, bugs):
    bug_of = {}
    for b in bugs:
        for t in b["_tests"]:
            bug_of.setdefault(t, []).append(b.get("bug_id", "?"))
    rows = []
    for c in cases:
        r = res.get(c["id"], {"status": "not run", "message": ""})
        rows.append({**c, "status": r["status"], "actual": r["message"], "bugs": bug_of.get(c["id"], [])})

    def counts(rs):
        k = {s: sum(r["status"] == s for r in rs) for s in ("passed", "failed", "error", "skipped", "not run")}
        k["total"] = len(rs)
        k["executed"] = k["passed"] + k["failed"] + k["error"]
        return k

    allc = counts(rows)
    mods = OrderedDict()
    for r in rows:
        mods.setdefault(r["module"], []).append(r)

    md = [f"# API Test Report — {doc.get('project', 'API')}", "",
          f"Environment: {doc.get('environment', '')} · Source: {doc.get('source', '')} · Date: {doc.get('date', '')}", "",
          "## 1. Overall result", "",
          "| Total | Passed | Failed | Errors | Skipped | Not run | Pass rate |", "|---|---|---|---|---|---|---|",
          f"| {allc['total']} | {allc['passed']} | {allc['failed']} | {allc['error']} | {allc['skipped']} | "
          f"{allc['not run']} | {pct(allc['passed'], allc['executed'])} |", ""]
    md += ["| Scenario type | Total | Passed | Failed | Pass rate |", "|---|---|---|---|---|"]
    for t in TYPES:
        k = counts([r for r in rows if r["type"] == t])
        md.append(f"| {t.capitalize()} | {k['total']} | {k['passed']} | {k['failed'] + k['error']} | {pct(k['passed'], k['executed'])} |")
    if bugs:
        by_sev = {s: sum(b.get("severity") == s for b in bugs if b.get("status") != "skipped") for s in SEV_ORDER}
        md += ["", "Bugs: " + " · ".join(f"{s} {n}" for s, n in by_sev.items() if n) +
               f" (total {sum(by_sev.values())})"]

    md += ["", "## 2. Module summary", "",
           "| Module | Endpoints | Positive | Negative | Total | Passed | Failed | Pass rate | Bugs |",
           "|---|---|---|---|---|---|---|---|---|"]
    for m, rs in mods.items():
        k = counts(rs)
        mb = sorted({b for r in rs for b in r["bugs"]})
        md.append(f"| {m} | {len({r['endpoint'] for r in rs})} | {sum(r['type'] == 'positive' for r in rs)} | "
                  f"{sum(r['type'] == 'negative' for r in rs)} | {k['total']} | {k['passed']} | "
                  f"{k['failed'] + k['error']} | {pct(k['passed'], k['executed'])} | {', '.join(mb) or '–'} |")

    md += ["", "## 3. Module details"]
    for m, rs in mods.items():
        k = counts(rs)
        md += ["", f"### {m} — {k['passed']}/{k['total']} passed"]
        if (doc.get("modules") or {}).get(m):
            md += ["", doc["modules"][m]]
        for t in TYPES:
            group = [r for r in rs if r["type"] == t]
            if not group:
                continue
            md += ["", f"#### {t.capitalize()} scenarios ({len(group)})", "",
                   "| ID | Scenario | Endpoint | Expected | Result | Actual (if failed) | Bug |",
                   "|---|---|---|---|---|---|---|"]
            md += [f"| {r['id']} | {cell(r['title'])} | `{cell(r['endpoint'])}` | {cell(r['expected'])} | "
                   f"{ICON[r['status']]} | {cell(r['actual']) if r['status'] in ('failed', 'error') else ''} | "
                   f"{', '.join(r['bugs']) or ''} |" for r in group]

    if bugs:
        md += ["", "## 4. Bugs found", "",
               "| Bug | Severity | Title | In simple words | Failed tests | Status |", "|---|---|---|---|---|---|"]
        bugs = sorted(bugs, key=lambda b: (SEV_ORDER.index(b["severity"]) if b.get("severity") in SEV_ORDER else 9,
                                           b.get("bug_id", "")))
        for b in bugs:
            tr = b.get("tracker") or {}
            status = b.get("status", "draft") + (f" — {tr.get('key')}" if tr.get("key") else "")
            md.append(f"| {b.get('bug_id')} | {b.get('severity')} | {cell(b.get('title'))} | "
                      f"{cell(b.get('description'))} | {', '.join(b['_tests'])} | {cell(status)} |")

    failed_no_bug = [r["id"] for r in rows if r["status"] in ("failed", "error") and not r["bugs"]]
    planned = {c["id"] for c in cases}
    extra = sorted({c["test_id"] for c in unplanned} | (set(res) - planned)) if res else []
    no_id = [c["name"] for c in unplanned]
    notes = []
    if failed_no_bug:
        notes.append(f"Failed with no bug linked (triage pending, test issue or env issue): {', '.join(failed_no_bug)}")
    if allc["not run"]:
        notes.append("Planned but not run: " + ", ".join(r["id"] for r in rows if r["status"] == "not run"))
    if extra:
        notes.append("Ran but not in test-cases.json: " + ", ".join(extra))
    if no_id:
        notes.append(f"{len(no_id)} test(s) without a test-case ID in the name: " + ", ".join(no_id[:10]))
    if notes:
        md += ["", "## 5. Notes for triage", ""] + [f"- {n}" for n in notes]
    if doc.get("assumptions"):
        md += ["", "## 6. Assumptions and open questions", ""] + [f"- {a}" for a in doc["assumptions"]]
    return "\n".join(md) + "\n", rows, allc


def write_csv(path, rows):
    cols = ["id", "module", "endpoint", "type", "category", "priority", "title", "request", "expected",
            "status", "actual", "bugs"]
    with open(path, "w", newline="", encoding="utf-8-sig") as f:  # -sig so Excel shows UTF-8 correctly
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "bugs": ", ".join(r["bugs"])})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("junit", nargs="*", help="JUnit XML file(s) or folder(s)")
    ap.add_argument("--cases", required=True, help="test-cases.json")
    ap.add_argument("--bugs", help="folder with BUG-*.json (default: <out>/bugs)")
    ap.add_argument("--out", default=".")
    ap.add_argument("--plan-only", action="store_true", help="only write test-cases.md")
    args = ap.parse_args()

    doc, cases = load_cases(args.cases)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "test-cases.md").write_text(render_plan(doc, cases), encoding="utf-8")
    pos = sum(c["type"] == "positive" for c in cases)
    print(f"Plan: {len(cases)} cases ({pos} positive, {len(cases) - pos} negative) -> {out / 'test-cases.md'}")
    if args.plan_only:
        return
    if not args.junit:
        die("give JUnit XML file(s), or use --plan-only")
    res, unplanned = results_by_id(args.junit)
    bugs = load_bugs(args.bugs or out / "bugs")
    md, rows, k = render_report(doc, cases, res, unplanned, bugs)
    (out / "test-report.md").write_text(md, encoding="utf-8")
    write_csv(out / "test-report.csv", rows)
    print(f"Report: {k['passed']} passed, {k['failed'] + k['error']} failed, {k['not run']} not run, "
          f"{len(bugs)} bug file(s) -> {out / 'test-report.md'}, {out / 'test-report.csv'}")


if __name__ == "__main__":
    main()
