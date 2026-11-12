from __future__ import annotations

from datetime import date
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEX_PATH = ROOT / "fieldex.json"
CATEGORIES = [
    "probability",
    "math",
    "logic",
    "history",
    "geography",
    "data",
    "security",
    "corinthians",
    "worldcup",
    "football",
]
RARITIES = ["common", "uncommon", "rare", "epic", "legendary"]
TEXT_FIELDS = ["title", "fact", "why"]


def validate_dex(data: dict[str, Any]) -> dict[str, Any]:
    """Validate the FielDex document and return it unchanged."""
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("entries must be a non-empty list")

    started = data.get("started")
    if not isinstance(started, str):
        raise ValueError("started must be an ISO date")
    date.fromisoformat(started)

    seen_ids: set[int] = set()
    for position, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise ValueError(f"Entry {position} must be an object")

        entry_id = entry.get("id")
        if not isinstance(entry_id, int) or entry_id <= 0:
            raise ValueError(f"Entry {position} has an invalid id")
        if entry_id in seen_ids:
            raise ValueError(f"Duplicate entry id: {entry_id}")
        seen_ids.add(entry_id)

        entry_date = entry.get("date")
        if not isinstance(entry_date, str):
            raise ValueError(f"Entry {entry_id} has an invalid date")
        date.fromisoformat(entry_date)

        if entry.get("category") not in CATEGORIES:
            raise ValueError(f"Entry {entry_id} has an invalid category")
        if entry.get("rarity") not in RARITIES:
            raise ValueError(f"Entry {entry_id} has an invalid rarity")

        for field in TEXT_FIELDS:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Entry {entry_id} has an empty {field}")

        tags = entry.get("tags")
        if not isinstance(tags, list) or not all(
            isinstance(tag, str) and tag.strip() for tag in tags
        ):
            raise ValueError(f"Entry {entry_id} has invalid tags")

        translations = entry.get("i18n", {})
        if not isinstance(translations, dict):
            raise ValueError(f"Entry {entry_id} has invalid translations")
        for language, translated in translations.items():
            if not isinstance(language, str) or not isinstance(translated, dict):
                raise ValueError(f"Entry {entry_id} has an invalid translation")
            for field in TEXT_FIELDS:
                if field in translated and (
                    not isinstance(translated[field], str)
                    or not translated[field].strip()
                ):
                    raise ValueError(
                        f"Entry {entry_id} has an empty {language}.{field}"
                    )

    expected_ids = list(range(1, len(entries) + 1))
    actual_ids = [entry["id"] for entry in entries]
    if actual_ids != expected_ids:
        raise ValueError("Entry ids must be ordered and contiguous from 1")

    return data


def load_dex(path: Path = DEX_PATH) -> dict[str, Any]:
    """Load and validate a FielDex JSON document."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("FielDex root must be an object")
    return validate_dex(data)
