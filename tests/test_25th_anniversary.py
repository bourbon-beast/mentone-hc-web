"""Regression: 25th Anniversary Team must not mangle lineups via markdown2."""

import re
import unittest
from pathlib import Path

import generate_history_pages as ghp

ROOT = Path(__file__).resolve().parents[1]


class AnniversaryContentTests(unittest.TestCase):
    def test_content_preserves_mens_half_line(self):
        html = ghp.anniversary_content_html()
        self.assertIn("<strong>Mark Thompson</strong> Right Half", html)
        self.assertIn("<strong>Gordon Tansey</strong>* Centre Half", html)
        self.assertIn("<strong>Roger Blasse</strong> Left Half", html)
        # markdown2 corruption signatures from **Name*** / --- Setext path
        self.assertNotIn("**Mark Thompson**", html)
        self.assertNotIn("<em><strong> Fullback", html)
        self.assertNotIn("<h2><strong>Clyde Beamish</strong>", html)

    def test_content_fixes_legacy_export_glitches(self):
        html = ghp.anniversary_content_html()
        self.assertIsNone(re.search(r"Fullba(?!ck)", html))
        self.assertIn("Fullback", html)
        self.assertIn("Jackie Anderton", html)
        self.assertIsNone(re.search(r"Anderto(?!n)", html))

    def test_shipped_page_matches_generator_guards(self):
        shipped = (ROOT / "history" / "25th-anniversary-team.html").read_text(encoding="utf-8")
        self.assertIn("<strong>Mark Thompson</strong> Right Half", shipped)
        self.assertNotIn("**Mark Thompson**", shipped)
        self.assertIsNone(re.search(r"Fullba(?!ck)", shipped))
        self.assertIn("Jackie Anderton", shipped)
        self.assertIn('href="life-members.html"', shipped)


if __name__ == "__main__":
    unittest.main()
