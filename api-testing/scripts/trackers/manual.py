"""Manual / export adapter: for any tool without an adapter yet (Azure DevOps, ClickUp, Redmine, Excel...).
'create' writes a ready-to-paste Markdown report and appends a CSV row; nothing is sent anywhere."""
import csv
from pathlib import Path

from .common import DUPLICATE_THRESHOLD, Tracker, similarity


class Manual(Tracker):
    name = "manual"
    description_format = "markdown"

    def _dir(self):
        d = Path(self.s.get("output_dir") or Path(self.common["reports_dir"]) / "bugs" / "export")
        return d if d.is_absolute() else Path(self.common["config_dir"]) / d

    def target(self):
        return f"local export folder {self._dir()} (copy into: {self.s.get('tool_name') or 'your bug tracker'})"

    def build_payload(self, bug):
        return {"bug_id": bug.get("bug_id", "BUG"), "title": self.title(bug), "severity": bug["severity"],
                "priority": bug.get("priority", ""), "description": self.description(bug)}

    def preview_fields(self, p):
        return [("Title", p["title"]), ("Severity", p["severity"]), ("Priority", p["priority"])]

    def preview_description(self, p):
        return p["description"]

    def find_duplicates(self, title):
        csv_path = self._dir() / "bugs.csv"
        if not csv_path.exists():
            return []
        with csv_path.open(encoding="utf-8") as f:
            return [{"key": r["bug_id"], "title": r["title"], "url": r["file"], "similarity": similarity(title, r["title"])}
                    for r in csv.DictReader(f) if similarity(title, r["title"]) >= DUPLICATE_THRESHOLD]

    def create(self, payload):
        d = self._dir()
        d.mkdir(parents=True, exist_ok=True)
        md = d / f"{payload['bug_id']}.md"
        md.write_text(f"# {payload['title']}\n\n{payload['description']}\n", encoding="utf-8")
        csv_path = d / "bugs.csv"
        new = not csv_path.exists()
        with csv_path.open("a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["bug_id", "title", "severity", "priority", "file"])
            if new:
                w.writeheader()
            w.writerow({"bug_id": payload["bug_id"], "title": payload["title"], "severity": payload["severity"],
                        "priority": payload["priority"], "file": str(md)})
        return {"id": payload["bug_id"], "key": payload["bug_id"], "url": str(md)}

    def doctor(self):
        return [f"Export folder: {self._dir()} (no network needed)"]
