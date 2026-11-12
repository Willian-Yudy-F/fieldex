from __future__ import annotations

import json
from pathlib import Path

from fieldex_core import load_dex


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "fieldex-data.js"


def main() -> int:
    data = load_dex()
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    OUTPUT.write_text(f"window.FIELD_DEX_INLINE = {payload};\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.name} with {len(data['entries'])} entries.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
