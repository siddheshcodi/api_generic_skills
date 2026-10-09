#!/usr/bin/env python3
"""
Detect which API test framework a project already uses.

Usage:  python detect_stack.py [project_dir]
Prints a JSON verdict: {"framework": "pytest|playwright|restassured|none", "evidence": [...], ...}
Standard library only.
"""
import json
import sys
from pathlib import Path

SKIP = {"node_modules", ".git", ".venv", "venv", "target", "build", "dist", "__pycache__", ".idea"}


def files(root, max_depth=4):
    root = Path(root)
    stack = [(root, 0)]
    while stack:
        d, depth = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP and depth < max_depth:
                    stack.append((e, depth + 1))
            else:
                yield e


def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")[:200_000]
    except OSError:
        return ""


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    score = {"pytest": 0, "playwright": 0, "restassured": 0}
    evidence = {k: [] for k in score}
    langs = set()
    for f in files(root):
        name, rel = f.name, str(f.relative_to(root))
        if name in ("pytest.ini", "conftest.py") or (name in ("pyproject.toml", "setup.cfg", "tox.ini") and "pytest" in read(f)):
            score["pytest"] += 2; evidence["pytest"].append(rel)
        if name.startswith("requirements") and name.endswith(".txt"):
            langs.add("python")
            txt = read(f).lower()
            if "pytest" in txt:
                score["pytest"] += 2; evidence["pytest"].append(rel)
        if name.startswith("test_") and name.endswith(".py"):
            langs.add("python")
            if "requests" in read(f) or "httpx" in read(f):
                score["pytest"] += 1; evidence["pytest"].append(rel)
        if name == "package.json":
            langs.add("javascript")
            txt = read(f)
            if "@playwright/test" in txt:
                score["playwright"] += 3; evidence["playwright"].append(rel)
        if name.startswith("playwright.config."):
            score["playwright"] += 2; evidence["playwright"].append(rel)
        if name in ("pom.xml", "build.gradle", "build.gradle.kts"):
            langs.add("java")
            if "rest-assured" in read(f):
                score["restassured"] += 3; evidence["restassured"].append(rel)
        if name.endswith(".java") and "io.restassured" in read(f):
            score["restassured"] += 1; evidence["restassured"].append(rel)
    best = max(score, key=score.get)
    framework = best if score[best] > 0 else "none"
    if framework == "none":
        suggestion = {"java": "restassured", "javascript": "playwright"}.get(
            next((l for l in ("java", "javascript") if l in langs), ""), "pytest")
    else:
        suggestion = framework
    print(json.dumps({
        "project": str(root), "framework": framework, "scores": score,
        "evidence": {k: v[:8] for k, v in evidence.items() if v},
        "languages_seen": sorted(langs), "suggested_framework": suggestion,
        "note": "Existing suite found - follow its structure." if framework != "none"
                else "No API test suite found - confirm suggested_framework with the user.",
    }, indent=2))


if __name__ == "__main__":
    main()
