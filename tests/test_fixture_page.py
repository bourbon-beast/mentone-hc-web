import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class FixturePageResultRenderingTests(unittest.TestCase):
    def test_fixture_page_supports_scraped_result_codes(self):
        fixtures = json.loads((REPO_ROOT / "fixtures.json").read_text())
        result_codes = {
            fixture["result"]
            for section in fixtures["sections"]
            for grade in section["grades"]
            for fixture in grade["fixtures"]
            if fixture["result"]
        }

        self.assertTrue(result_codes)
        self.assertLessEqual(result_codes, {"W", "L", "D"})

        fixtures_html = (REPO_ROOT / "fixtures.html").read_text()
        for code, class_name, label in (
            ("W", "win", "Win"),
            ("L", "loss", "Loss"),
            ("D", "draw", "Draw"),
        ):
            self.assertIn(
                f"{code}: {{ className: '{class_name}', label: '{label}' }}",
                fixtures_html,
            )


if __name__ == "__main__":
    unittest.main()
