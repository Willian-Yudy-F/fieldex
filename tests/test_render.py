from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import generate_card
from fieldex_core import load_dex


class RenderTests(unittest.TestCase):
    def test_latest_card_renders_with_pillow(self) -> None:
        original_output = generate_card.OUT
        try:
            with tempfile.TemporaryDirectory() as directory:
                generate_card.OUT = Path(directory)
                output = generate_card.draw_card(load_dex()["entries"][-1])
                self.assertTrue(output.is_file())
                self.assertGreater(output.stat().st_size, 10_000)
        finally:
            generate_card.OUT = original_output


if __name__ == "__main__":
    unittest.main()
