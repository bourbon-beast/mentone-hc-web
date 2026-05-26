import json
import unittest
from pathlib import Path

from bs4 import BeautifulSoup

from scripts.update_fixtures import PageValidationError, validate_team_page


ROOT = Path(__file__).resolve().parents[1]


class FixtureSourceTests(unittest.TestCase):
    def test_validate_team_page_rejects_wrong_team_title(self):
        soup = BeautifulSoup(
            "<h2>2026 Senior Competition · Mens Pennant E South East - 2026 Mornington Peninsula Hockey Club</h2>",
            "html.parser",
        )

        with self.assertRaises(PageValidationError):
            validate_team_page(
                soup,
                "2026 Junior Competition · U18 Mixed District SE - 2026 Mentone Hockey Club",
                "U18 Mixed",
            )

    def test_all_configured_sources_expect_mentone_pages(self):
        config = json.loads((ROOT / "scripts" / "mentone_teams_2026.json").read_text())

        for section in config["sections"]:
            for grade in section["grades"]:
                with self.subTest(section=section["id"], grade=grade["grade"]):
                    self.assertIn("expected_title", grade)
                    self.assertIn("Mentone Hockey Club", grade["expected_title"])

    def test_render_supports_win_loss_draw_markers(self):
        html = (ROOT / "fixtures.html").read_text()

        self.assertIn("if (result === 'W')", html)
        self.assertIn("if (result === 'L')", html)
        self.assertIn("if (result === 'D')", html)


if __name__ == "__main__":
    unittest.main()
