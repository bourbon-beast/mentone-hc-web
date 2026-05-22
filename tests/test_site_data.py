import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteDataTests(unittest.TestCase):
    def load_json(self, relative_path):
        with (ROOT / relative_path).open(encoding="utf-8") as fh:
            return json.load(fh)

    def test_news_json_is_valid_and_populated(self):
        data = self.load_json("news.json")

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_fixture_grades_are_not_silently_empty(self):
        data = self.load_json("fixtures.json")

        empty_grades = [
            f"{section['label']} / {grade['grade']}"
            for section in data["sections"]
            for grade in section["grades"]
            if not grade["fixtures"]
        ]

        self.assertEqual(empty_grades, [])

    def test_fixture_config_declares_expected_team_titles(self):
        config = self.load_json("scripts/mentone_teams_2026.json")

        missing = [
            f"{section['label']} / {grade['grade']}"
            for section in config["sections"]
            for grade in section["grades"]
            if not grade.get("expected_title")
        ]

        self.assertEqual(missing, [])
        self.assertEqual(
            config["sections"][1]["grades"][0]["team_url"],
            "https://www.hockeyvictoria.org.au/games/team/25879/409899",
        )

    def test_fixture_results_match_renderer_schema(self):
        data = self.load_json("fixtures.json")
        bad_results = [
            (section["label"], grade["grade"], fixture.get("result"))
            for section in data["sections"]
            for grade in section["grades"]
            for fixture in grade["fixtures"]
            if fixture.get("result") is not None
            and not re.match(r"^(W|L|D|\d+\s*-\s*\d+)$", fixture["result"])
        ]

        self.assertEqual(bad_results, [])

    def test_fixture_renderer_handles_scraped_outcomes(self):
        html = (ROOT / "fixtures.html").read_text(encoding="utf-8")

        self.assertIn("outcome === 'W'", html)
        self.assertIn("outcome === 'L'", html)
        self.assertIn("outcome === 'D'", html)


if __name__ == "__main__":
    unittest.main()
