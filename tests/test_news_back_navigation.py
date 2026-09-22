"""Regression: article Back control must reach renderNews outside the IIFE."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NewsBackNavigationTests(unittest.TestCase):
    def test_back_button_calls_render_news(self) -> None:
        html = (ROOT / "news.html").read_text(encoding="utf-8")
        self.assertIn('onclick="renderNews()"', html)

    def test_render_news_is_exposed_on_window(self) -> None:
        html = (ROOT / "news.html").read_text(encoding="utf-8")
        self.assertRegex(
            html,
            r"window\.renderNews\s*=\s*function\s+renderNews\s*\(",
        )
        # Local-only declaration would leave inline onclick broken.
        self.assertIsNone(
            re.search(r"(?m)^\s*function\s+renderNews\s*\(", html),
            "renderNews must not be IIFE-local only",
        )


if __name__ == "__main__":
    unittest.main()
