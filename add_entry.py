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

from fieldex_core import CATEGORIES, RARITIES, load_dex, validate_dex

ROOT = Path(__file__).parent
DEX = ROOT / "fieldex.json"

def ask(prompt, options=None, required=False):
    if options:
        print(f"\n{prompt}")
        for i, o in enumerate(options, 1):
            print(f"  {i}. {o}")
        while True:
            raw = input("> ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            print("  pick a number from the list")
    while True:
        value = input(f"\n{prompt}\n> ").strip()
        if value or not required:
            return value
        print("  this field cannot be empty")


def main():
    original_json = DEX.read_text(encoding="utf-8")
    data = load_dex(DEX)
    next_id = max((e["id"] for e in data["entries"]), default=0) + 1

    print(f"=== FielDex :: capturing entry #{next_id:03d} ===")
    entry = {
        "id": next_id,
        "date": date.today().isoformat(),
        "category": ask("Category?", CATEGORIES),
        "rarity": ask("Rarity?", RARITIES),
        "title": ask("Title (short, punchy)", required=True),
        "fact": ask("The fact (1-3 sentences)", required=True),
        "why": ask("Why it matters / the intuition", required=True),
        "tags": [t.strip() for t in ask("Tags (comma separated)").split(",") if t.strip()],
    }

    data["entries"].append(entry)
    validate_dex(data)
    DEX.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSaved entry #{next_id:03d} to fieldex.json")

    # auto-generate the card
    print("Generating card...")
    try:
        subprocess.run(
            [sys.executable, str(ROOT / "generate_card.py"), str(next_id)],
            check=True,
        )
        subprocess.run(
            [sys.executable, str(ROOT / "build_data_js.py")],
            check=True,
        )
    except subprocess.CalledProcessError as error:
        DEX.write_text(original_json, encoding="utf-8")
        for generated_card in (ROOT / "cards").glob(f"fieldex_{next_id:03d}_*.png"):
            generated_card.unlink()
        print(f"Generation failed; restored fieldex.json: {error}", file=sys.stderr)
        return 1
    print("\nDone! Commit it:")
    print(f'  git add . && git commit -m "dex #{next_id:03d}: {entry["title"]}" && git push')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
