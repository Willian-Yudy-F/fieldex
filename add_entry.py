"""
FielDex - Quick entry adder
===========================
Adds a new knowledge entry to fieldex.json without editing JSON by hand,
auto-assigning the next id and today's date, then generates its card.

Usage:
    python add_entry.py
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DEX = ROOT / "fieldex.json"

CATEGORIES = ["probability", "math", "logic", "history",
              "geography", "data", "security", "corinthians", "worldcup"]
RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]


def ask(prompt, options=None):
    if options:
        print(f"\n{prompt}")
        for i, o in enumerate(options, 1):
            print(f"  {i}. {o}")
        while True:
            raw = input("> ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            print("  pick a number from the list")
    return input(f"\n{prompt}\n> ").strip()


def main():
    data = json.loads(DEX.read_text(encoding="utf-8"))
    next_id = max((e["id"] for e in data["entries"]), default=0) + 1

    print(f"=== FielDex :: capturing entry #{next_id:03d} ===")
    entry = {
        "id": next_id,
        "date": date.today().isoformat(),
        "category": ask("Category?", CATEGORIES),
        "rarity": ask("Rarity?", RARITIES),
        "title": ask("Title (short, punchy)"),
        "fact": ask("The fact (1-3 sentences)"),
        "why": ask("Why it matters / the intuition"),
        "tags": [t.strip() for t in ask("Tags (comma separated)").split(",") if t.strip()],
    }

    data["entries"].append(entry)
    DEX.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved entry #{next_id:03d} to fieldex.json")

    # auto-generate the card
    print("Generating card...")
    subprocess.run([sys.executable, str(ROOT / "generate_card.py"), str(next_id)])
    print("\nDone! Commit it:")
    print(f'  git add . && git commit -m "dex #{next_id:03d}: {entry["title"]}" && git push')


if __name__ == "__main__":
    main()
