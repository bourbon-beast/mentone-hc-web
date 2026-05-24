import importlib.util
import json
import pathlib
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parents[1]


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path):
    return json.loads(read_text(path))


class StaticRegressionTests(unittest.TestCase):
    def test_news_json_is_valid(self):
        data = read_json("news.json")

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_news_filters_do_not_use_inline_handlers(self):
        html = read_text("news.html")

        self.assertNotIn("onclick=\"filterNews('", html)
        self.assertIn('data-category="${c}"', html)
        self.assertIn("addEventListener('click'", html)

    def test_fixtures_json_has_no_empty_grades_or_self_opponents(self):
        data = read_json("fixtures.json")

        for section in data["sections"]:
            for grade in section["grades"]:
                label = f"{section['label']} {grade['grade']}"
                self.assertGreater(len(grade["fixtures"]), 0, label)
                for fixture in grade["fixtures"]:
                    self.assertNotEqual(
                        fixture.get("opponent"),
                        "Mentone Hockey Club",
                        label,
                    )

    def test_fixtures_renderer_handles_scraper_result_codes(self):
        html = read_text("fixtures.html")

        self.assertIn("result === 'W'", html)
        self.assertIn("result === 'L'", html)
        self.assertIn("result === 'D'", html)

    def test_fixture_config_has_expected_team_title_guards(self):
        config = read_json("scripts/mentone_teams_2026.json")
        urls_by_grade = {
            (section["label"], grade["grade"]): grade
            for section in config["sections"]
            for grade in section["grades"]
        }

        self.assertEqual(
            urls_by_grade[("Women's", "Premier League")]["team_url"],
            "https://www.hockeyvictoria.org.au/games/team/25879/409899",
        )
        self.assertEqual(
            urls_by_grade[("Juniors", "U18 Mixed")]["team_url"],
            "https://www.hockeyvictoria.org.au/games/team/26323/418103",
        )
        self.assertEqual(
            urls_by_grade[("Masters", "Men's 40+ BSE")]["team_url"],
            "https://www.hockeyvictoria.org.au/games/team/26185/416550",
        )

        for key, grade in urls_by_grade.items():
            self.assertIn("Mentone", grade.get("expected_title", ""), key)


class FixtureScraperValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location(
            "update_fixtures",
            ROOT / "scripts" / "update_fixtures.py",
        )
        cls.update_fixtures = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.update_fixtures)

    def test_fetch_soup_rejects_non_ok_empty_responses(self):
        class Response:
            status_code = 202
            text = ""

            def raise_for_status(self):
                raise AssertionError("raise_for_status should not be reached")

        with mock.patch.object(
            self.update_fixtures.requests,
            "get",
            return_value=Response(),
        ):
            with self.assertRaisesRegex(
                self.update_fixtures.ScrapeValidationError,
                "unexpected HTTP 202",
            ):
                self.update_fixtures.fetch_soup("https://example.invalid/team")

    def test_validate_team_page_rejects_wrong_team(self):
        soup = self.update_fixtures.BeautifulSoup(
            "<h1>2026 Senior Competition - Monash University Hockey Club</h1>",
            "html.parser",
        )

        with self.assertRaisesRegex(
            self.update_fixtures.ScrapeValidationError,
            "did not match expected title",
        ):
            self.update_fixtures.validate_team_page(
                soup,
                "Womens Metro 1 South - 2026 Mentone Hockey Club",
                "Metro",
                "https://example.invalid/team",
            )


if __name__ == "__main__":
    unittest.main()
