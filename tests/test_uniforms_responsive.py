import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def declarations(css, selector):
    matches = re.findall(
        rf"(?:^|\}})\s*{re.escape(selector)}\s*\{{([^}}]+)\}}",
        css,
        flags=re.MULTILINE,
    )
    return "\n".join(matches)


class UniformsResponsiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.css = (ROOT / "site.css").read_text(encoding="utf-8")
        cls.html = (ROOT / "uniforms.html").read_text(encoding="utf-8")

    def test_wide_clash_table_is_horizontally_scrollable(self):
        table_rules = declarations(self.css, ".uniform-clash-table")
        wrapper_rules = declarations(self.css, ".uniform-clash-table-wrap")

        self.assertRegex(table_rules, r"min-width\s*:\s*620px")
        self.assertRegex(wrapper_rules, r"overflow-x\s*:\s*auto")

    def test_clash_table_contains_both_required_guides(self):
        self.assertIn("Shirt / top clashes", self.html)
        self.assertIn("Sock clashes", self.html)
        self.assertIn("uniform-clash-list--socks", self.html)


if __name__ == "__main__":
    unittest.main()
