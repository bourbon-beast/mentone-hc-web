import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def read_json(relative_path):
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


class StaticRegressionTests(unittest.TestCase):
    def test_news_json_is_valid(self):
        data = read_json("news.json")

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_news_category_filters_do_not_use_fragile_inline_handlers(self):
        html = read_text("news.html")

        self.assertIn("data-news-filter", html)
        self.assertIn("newsContent.addEventListener('click'", html)
        self.assertNotIn('onclick="filterNews', html)

    def test_fixture_result_codes_render_with_correct_outcome_classes(self):
        html = read_text("fixtures.html")

        self.assertIn("const RESULT_CODES", html)
        self.assertIn("W: { cls: 'win', label: 'Win' }", html)
        self.assertIn("L: { cls: 'loss', label: 'Loss' }", html)
        self.assertIn("D: { cls: 'draw', label: 'Draw' }", html)

    def test_fixture_sources_have_mentone_title_contracts(self):
        config = read_json("scripts/mentone_teams_2026.json")
        expected_competitions = {
            "mens": "/games/team/25879/",
            "womens": "/games/team/25879/",
            "juniors": "/games/team/26323/",
            "masters": "/games/team/26185/",
        }

        for section in config["sections"]:
            expected_path = expected_competitions[section["id"]]
            for grade in section["grades"]:
                with self.subTest(section=section["id"], grade=grade["grade"]):
                    self.assertIn(expected_path, grade["team_url"])
                    self.assertIn("Mentone Hockey Club", grade["expected_title"])

    def test_generated_fixtures_match_config_and_have_no_empty_grades(self):
        config = read_json("scripts/mentone_teams_2026.json")
        fixtures = read_json("fixtures.json")

        self.assertEqual(
            [section["id"] for section in config["sections"]],
            [section["id"] for section in fixtures["sections"]],
        )

        for config_section, fixture_section in zip(config["sections"], fixtures["sections"]):
            self.assertEqual(config_section["label"], fixture_section["label"])
            self.assertEqual(config_section["color"], fixture_section["color"])
            self.assertEqual(
                [grade["grade"] for grade in config_section["grades"]],
                [grade["grade"] for grade in fixture_section["grades"]],
            )

            for grade in fixture_section["grades"]:
                with self.subTest(section=fixture_section["id"], grade=grade["grade"]):
                    self.assertGreater(len(grade["fixtures"]), 0)


if __name__ == "__main__":
    unittest.main()
