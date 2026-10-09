#!/usr/bin/env python3
"""
Parse JUnit XML results (pytest --junitxml, Playwright junit reporter, Maven/Gradle surefire)
into a summary and a failure list ready for triage.

Usage:
  python parse_results.py <junit.xml> [more.xml or folder ...] [--out DIR]

Writes DIR/summary.md and DIR/failures.json (default DIR=./results). Standard library only.
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ID_RE = re.compile(r"\b([A-Z][A-Z0-9]*[-_][A-Z0-9]+[-_]\d{2,4})\b")


def collect(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += sorted(p.rglob("*.xml"))
        elif p.exists():
            files.append(p)
        else:
            print(f"WARNING: {p} not found", file=sys.stderr)
    return files


def parse(files):
    cases = []
    for f in files:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError as e:
            print(f"WARNING: cannot parse {f}: {e}", file=sys.stderr)
            continue
        for tc in root.iter("testcase"):
            name = tc.get("name", "")
            classname = tc.get("classname", "")
            status, message, details = "passed", "", ""
            for tag in ("failure", "error", "skipped"):
                el = tc.find(tag)
                if el is not None:
                    status = {"failure": "failed", "error": "error", "skipped": "skipped"}[tag]
                    message = (el.get("message") or "").strip()
                    details = (el.text or "").strip()
                    break
            m = ID_RE.search(name.replace("_", "-")) or ID_RE.search(classname.replace("_", "-"))
            test_id = m.group(1).replace("_", "-") if m else ""
            cases.append({
                "test_id": test_id, "name": name, "classname": classname,
                "file": tc.get("file", ""), "time_s": float(tc.get("time") or 0),
                "status": status, "message": message[:1000], "details": details[-3000:],
                "stdout": ((tc.findtext("system-out") or "").strip())[-1500:],
                "source_report": str(f),
            })
    return cases


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()

    files = collect(args.paths)
    if not files:
        sys.exit("ERROR: no JUnit XML files found")
    cases = parse(files)
    counts = {s: sum(1 for c in cases if c["status"] == s) for s in ("passed", "failed", "error", "skipped")}
    total = len(cases)
    executed = total - counts["skipped"]
    rate = round(100 * counts["passed"] / executed, 1) if executed else 0.0
    duration = round(sum(c["time_s"] for c in cases), 1)
    problems = [c for c in cases if c["status"] in ("failed", "error")]

    # Hint for triage: many failures with same message -> likely environment/common cause
    groups = {}
    for c in problems:
        key = (c["message"] or c["details"][:120]).split("\n")[0][:120]
        groups.setdefault(key, []).append(c["test_id"] or c["name"])

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "failures.json").write_text(json.dumps({
        "summary": {**counts, "total": total, "pass_rate": rate, "duration_s": duration},
        "failures": problems,
        "common_messages": {k: v for k, v in groups.items() if len(v) > 1},
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    md = ["# Test run results", "",
          "| Total | Passed | Failed | Errors | Skipped | Pass rate | Duration |", "|---|---|---|---|---|---|---|",
          f"| {total} | {counts['passed']} | {counts['failed']} | {counts['error']} | {counts['skipped']} | {rate}% | {duration}s |", ""]
    if problems:
        md += ["## Failures and errors (to triage)", "", "| Test ID | Test | Status | Message |", "|---|---|---|---|"]
        for c in problems:
            msg = (c["message"] or c["details"]).split("\n")[0][:160].replace("|", "\\|")
            md.append(f"| {c['test_id'] or '-'} | {c['name'][:80]} | {c['status']} | {msg} |")
        common = {k: v for k, v in groups.items() if len(v) > 1}
        if common:
            md += ["", "## Same message in several failures (check for environment/common cause first)"]
            for k, v in common.items():
                md.append(f"- {len(v)}x `{k}` -> {', '.join(v[:10])}{' ...' if len(v) > 10 else ''}")
    else:
        md.append("All executed tests passed.")
    (out / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:5]))
    print(f"\n{len(problems)} failure(s)/error(s) -> {out}/failures.json, {out}/summary.md")


if __name__ == "__main__":
    main()
