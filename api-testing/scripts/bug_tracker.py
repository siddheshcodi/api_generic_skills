#!/usr/bin/env python3
"""
Bug tracker CLI for the api-testing skill. Works with ProofHub, Jira, Trello, or a manual export,
chosen by `bug_tracker.type` in api-test.config.yaml.

SAFETY: `create` never sends anything unless `--confirm` is passed. Claude adds --confirm only
after the user explicitly approved that specific bug in chat.

Commands
  doctor                              check config, credentials and access
  lookup                              list available lookups for the tracker
  lookup NAME [--project/--board/--query X]   find IDs for the config (projects, lists, labels...)
  preview BUG.json [BUG.json ...]     show exactly what would be sent + duplicate check
  create  BUG.json --confirm          create ONE bug (refuses without --confirm)

Options
  --config PATH        api-test.config.yaml (default: search current dir and parents)
  --tracker NAME       override bug_tracker.type for this run (proofhub | jira | trello | manual)
  --offline            preview without contacting the tracker (no duplicate check)
  --allow-duplicate    create even if a similar open item exists (only after the user agrees)
  --save-payload PATH  also write the JSON payload to a file

Needs Python 3.8+ and PyYAML (pip install pyyaml).
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trackers import ADAPTERS  # noqa: E402
from trackers.common import SEVERITIES, TrackerError, die, mask  # noqa: E402

CONFIG_NAME = "api-test.config.yaml"
REQUIRED = ["title", "description", "severity", "method", "endpoint", "expected", "actual"]


# ----------------------------------------------------------------------------- setup
def find_config(explicit):
    if explicit:
        p = Path(explicit)
        if not p.is_file():
            die(f"Config not found: {p}")
        return p.resolve()
    for d in [Path.cwd(), *Path.cwd().parents]:
        if (d / CONFIG_NAME).is_file():
            return (d / CONFIG_NAME).resolve()
    die(f"{CONFIG_NAME} not found in {Path.cwd()} or parent folders. Use --config PATH.")


def load_config(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    try:
        import yaml  # type: ignore
    except ImportError:
        die("PyYAML is missing. Run: pip install pyyaml")
    return yaml.safe_load(text) or {}


def make_tracker(cfg, cfg_path, override):
    bt = cfg.get("bug_tracker") or {}
    kind = (override or bt.get("type") or "").lower()
    if not kind:
        die("Set bug_tracker.type in config (proofhub | jira | trello | manual).")
    if kind not in ADAPTERS:
        die(f"Unknown tracker '{kind}'. Available: {sorted(ADAPTERS)}. "
            f"Use 'manual' or add an adapter (references/trackers/adding-a-tracker.md).")
    common = {"title_prefix": bt.get("title_prefix", "[API]"),
              "reports_dir": (cfg.get("testing") or {}).get("reports_dir", "api-test-reports"),
              "config_dir": str(cfg_path.parent)}
    return ADAPTERS[kind](cfg.get(kind) or {}, common)


def load_bug(path):
    try:
        bug = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        die(f"Cannot read bug file {path}: {e}")
    missing = [k for k in REQUIRED if not bug.get(k)]
    if missing:
        die(f"{path}: missing required fields {missing} (see assets/bug.example.json)")
    if bug["severity"] not in SEVERITIES:
        die(f"{path}: severity must be one of {SEVERITIES}, got '{bug['severity']}'")
    return bug


# ----------------------------------------------------------------------------- output
def show_preview(tracker, bug, payload, path, dups):
    line = "=" * 78
    print(line)
    print(f"PREVIEW  {bug.get('bug_id', Path(path).stem)}   tracker: {tracker.name}   status: {bug.get('status', 'draft')}")
    print(line)
    print(f"Target   : {tracker.target()}")
    for label, value in tracker.preview_fields(payload):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        print(f"{label:<9}: {value}")
    print("-" * 78)
    print(tracker.preview_description(payload))
    print("-" * 78)
    if dups is None:
        print("Duplicate check: skipped (offline)")
    elif dups:
        print("POSSIBLE DUPLICATES (open items with similar titles):")
        for d in dups:
            print(f"  - {d['key']}  {d['title']}  (similarity {d['similarity']})  {d.get('url', '')}")
    else:
        print("Duplicate check: no similar open item found")
    print()


# ----------------------------------------------------------------------------- commands
def cmd_preview(tracker, args):
    problems = tracker.config_problems()
    for path in args.files:
        bug = load_bug(path)
        payload = tracker.build_payload(bug) if not problems else None
        if payload is None:
            die("; ".join(problems) + ". Fix the config (use the lookup command to find IDs).")
        dups = None if args.offline else tracker.find_duplicates(payload_title(tracker, bug))
        show_preview(tracker, bug, payload, path, dups)
        save_payload(args, path, payload)
    print("Nothing was sent. Create only after the user approves, with:")
    print("  python bug_tracker.py create <BUG.json> --confirm")


def payload_title(tracker, bug):
    return tracker.title(bug)


def save_payload(args, path, payload):
    if not args.save_payload:
        return
    out = Path(args.save_payload)
    if len(args.files) > 1:
        out = out.parent / f"{Path(path).stem}.payload.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Payload saved to {out}")


def cmd_create(tracker, args):
    if len(args.files) != 1:
        die("create takes exactly one bug file, so each bug is approved and created individually.")
    path = args.files[0]
    bug = load_bug(path)
    done = bug.get("tracker") or {}
    if bug.get("status") == "created":
        die(f"{path} was already created ({done.get('type')} {done.get('key')} {done.get('url', '')}). Not creating again.")
    if bug.get("status") == "skipped":
        die(f"{path} is marked 'skipped' by the user. Change status to 'draft' first if they changed their mind.")
    problems = tracker.config_problems()
    if problems:
        die("; ".join(problems) + ". Fix the config (use the lookup command to find IDs).")
    payload = tracker.build_payload(bug)

    if not args.confirm:
        show_preview(tracker, bug, payload, path, None if args.offline else tracker.find_duplicates(tracker.title(bug)))
        print("NOT CREATED: --confirm missing. Show this preview to the user; create only after explicit approval.")
        sys.exit(2)

    dups = tracker.find_duplicates(tracker.title(bug))
    if dups and not args.allow_duplicate:
        show_preview(tracker, bug, payload, path, dups)
        print("NOT CREATED: possible duplicate. Ask the user: add to existing / create anyway / skip.")
        print("If they choose 'create anyway', rerun with --allow-duplicate.")
        sys.exit(3)

    result = tracker.create(payload)
    bug["status"] = "created"
    bug["tracker"] = {"type": tracker.name, **result}
    Path(path).write_text(json.dumps(bug, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"CREATED in {tracker.name}: {result.get('key')} - {tracker.title(bug)}")
    if result.get("url"):
        print(f"Link: {result['url']}")
    print(f"Updated {path} (status 'created').")


def cmd_lookup(tracker, args):
    available = tracker.lookups()
    if not available:
        print(f"No lookups for '{tracker.name}'.")
        return
    name = args.files[0] if args.files else None
    if not name or name not in available:
        print(f"Lookups for {tracker.name}:")
        for k, (help_text, _) in available.items():
            print(f"  {k:<12} {help_text}")
        return
    rows = available[name][1](args)
    for row_id, label in rows:
        print(f"{row_id}\t{label}")
    if not rows:
        print("(nothing returned)")


def cmd_doctor(tracker, cfg_path):
    print(f"Config  : {cfg_path}")
    print(f"Tracker : {tracker.name} -> {tracker.target()}")
    problems = tracker.config_problems()
    for p in problems:
        print(f"Problem : {p}")
    if problems:
        print("Result  : fix the problems above")
        sys.exit(1)
    for line in tracker.doctor():
        print(f"OK      : {line}")
    print("Result  : ready")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["doctor", "lookup", "preview", "create"])
    ap.add_argument("files", nargs="*", help="bug JSON file(s), or the lookup name")
    ap.add_argument("--config")
    ap.add_argument("--tracker")
    ap.add_argument("--project")
    ap.add_argument("--board")
    ap.add_argument("--query")
    ap.add_argument("--confirm", action="store_true", help="REQUIRED to create. Only after user approval.")
    ap.add_argument("--allow-duplicate", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--save-payload")
    args = ap.parse_args()

    cfg_path = find_config(args.config)
    tracker = make_tracker(load_config(cfg_path), cfg_path, args.tracker)
    try:
        if args.command in ("preview", "create") and not args.files:
            die(f"{args.command} needs at least one bug JSON file.")
        {"preview": lambda: cmd_preview(tracker, args),
         "create": lambda: cmd_create(tracker, args),
         "lookup": lambda: cmd_lookup(tracker, args),
         "doctor": lambda: cmd_doctor(tracker, cfg_path)}[args.command]()
    except TrackerError as e:
        die(mask(str(e)))


if __name__ == "__main__":
    main()
