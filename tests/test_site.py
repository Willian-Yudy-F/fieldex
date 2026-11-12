from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class SiteTests(unittest.TestCase):
    def test_public_links_do_not_contain_placeholders(self) -> None:
        self.assertNotIn("SEU-LINKEDIN", HTML)
        self.assertNotIn("SEU-EMAIL", HTML)

    def test_accessibility_basics_are_present(self) -> None:
        self.assertIn("Skip to cards", HTML)
        self.assertIn("Search cards", HTML)
        self.assertIn("prefers-reduced-motion", HTML)
        self.assertIn('role="dialog"', HTML)

    def test_metadata_points_to_public_site(self) -> None:
        self.assertIn('rel="canonical"', HTML)
        self.assertIn("https://willian-yudy-f.github.io/fieldex/", HTML)


if __name__ == "__main__":
    unittest.main()
