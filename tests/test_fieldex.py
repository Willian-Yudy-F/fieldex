from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from fieldex_core import load_dex, validate_dex


ROOT = Path(__file__).resolve().parents[1]


def load_inline_data() -> dict[str, object]:
    script = (ROOT / "fieldex-data.js").read_text(encoding="utf-8")
    prefix = "window.FIELD_DEX_INLINE = "
    if not script.startswith(prefix) or not script.endswith(";\n"):
        raise AssertionError("fieldex-data.js has an unexpected wrapper")
    return json.loads(script[len(prefix) : -2])


class FieldDexTests(unittest.TestCase):
    def test_repository_data_is_valid(self) -> None:
        data = load_dex()
        self.assertEqual(len(data["entries"]), 42)
        self.assertEqual(data["entries"][-1]["id"], 42)

    def test_inline_fallback_matches_json(self) -> None:
        self.assertEqual(load_inline_data(), load_dex())

    def test_duplicate_ids_are_rejected(self) -> None:
        data = copy.deepcopy(load_dex())
        data["entries"][1]["id"] = data["entries"][0]["id"]
        with self.assertRaisesRegex(ValueError, "Duplicate entry id"):
            validate_dex(data)

    def test_empty_fact_is_rejected(self) -> None:
        data = copy.deepcopy(load_dex())
        data["entries"][0]["fact"] = " "
        with self.assertRaisesRegex(ValueError, "empty fact"):
            validate_dex(data)

    def test_entry_ids_are_contiguous(self) -> None:
        data = copy.deepcopy(load_dex())
        data["entries"][1]["id"] = 99
        with self.assertRaisesRegex(ValueError, "contiguous"):
            validate_dex(data)


if __name__ == "__main__":
    unittest.main()
