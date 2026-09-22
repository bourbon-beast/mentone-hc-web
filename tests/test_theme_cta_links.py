"""Regression: front-page theme CTAs must keep working href destinations."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "theme" / "mentone"
REGISTRATIONS = "https://www.revolutionise.com.au/mentonehockey/club-registrations"


def _anchor_for_label(html: str, label: str) -> str | None:
    pattern = re.compile(
        rf'<a\b([^>]*)>\s*{re.escape(label)}\s*</a>',
        re.IGNORECASE,
    )
    match = pattern.search(html)
    return match.group(1) if match else None


def _href(attrs: str) -> str | None:
    match = re.search(r'\bhref=["\']([^"\']+)["\']', attrs)
    return match.group(1) if match else None


class ThemeCtaLinksTests(unittest.TestCase):
    def test_front_page_composes_cta_patterns(self) -> None:
        front = (THEME / "templates" / "front-page.html").read_text(encoding="utf-8")
        self.assertIn('slug":"mentone/hero-home"', front)
        self.assertIn('slug":"mentone/cta-band"', front)

    def test_hero_home_new_players_cta_has_destination(self) -> None:
        html = (THEME / "patterns" / "hero-home.php").read_text(encoding="utf-8")
        attrs = _anchor_for_label(html, "New to hockey?")
        self.assertIsNotNone(attrs, "New to hockey? button missing")
        href = _href(attrs or "")
        self.assertEqual(href, "/new-players/")

    def test_cta_band_register_has_registration_url(self) -> None:
        html = (THEME / "patterns" / "cta-band.php").read_text(encoding="utf-8")
        attrs = _anchor_for_label(html, "Register now")
        self.assertIsNotNone(attrs, "Register now button missing")
        href = _href(attrs or "")
        self.assertEqual(href, REGISTRATIONS)

    def test_theme_patterns_have_no_href_less_cta_anchors(self) -> None:
        offenders: list[str] = []
        for path in (THEME / "patterns").glob("*.php"):
            text = path.read_text(encoding="utf-8")
            for match in re.finditer(r"<a\b([^>]*)>", text):
                attrs = match.group(1)
                if "wp-block-button__link" not in attrs:
                    continue
                if "href=" not in attrs:
                    line = text.count("\n", 0, match.start()) + 1
                    offenders.append(f"{path.name}:{line}")
        self.assertEqual(offenders, [], f"CTA anchors missing href: {offenders}")


if __name__ == "__main__":
    unittest.main()
