"""Rebuild LLM wiki index and SQLite knowledge DB from wiki/*.md files."""

import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
INDEX = ROOT / "index"
DB = ROOT / "data" / "knowledge.db"

def parse_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    data = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def main():
    topics = []
    for f in sorted(WIKI.glob("*.md")):
        if f.name == "00-INDEX.md":
            continue
        fm = parse_front_matter(f.read_text(encoding="utf-8"))
        topics.append({
            "id": fm.get("id", f.stem),
            "file": str(f.relative_to(ROOT)),
            "summary": fm.get("summary", f"Wiki topic: {f.stem}"),
            "tags": [t.strip() for t in fm.get("tags", "").strip("[]").split(",") if t.strip()],
            "updated": fm.get("updated", "")
        })

    (INDEX / "topics.json").write_text(json.dumps({"topics": topics}, ensure_ascii=False, indent=2), encoding="utf-8")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))
    for t in topics:
        cur.execute("INSERT OR REPLACE INTO topics (id,title,summary,tags,updated) VALUES (?,?,?,?,?)",
            (t["id"], t["id"], t["summary"], ",".join(t["tags"]), t["updated"]))
    conn.commit()
    conn.close()
    print(f"Rebuilt: {len(topics)} topics")

if __name__ == "__main__":
    main()
