import unittest
from unittest.mock import patch

from scripts import update_fixtures


def fixture_result(*grade_fixture_lists):
    return {
        "updated": "2026-05-18",
        "sections": [
            {
                "id": "mens",
                "label": "Men's",
                "color": "yellow",
                "grades": [
                    {"grade": f"Grade {idx}", "fixtures": fixtures}
                    for idx, fixtures in enumerate(grade_fixture_lists, start=1)
                ],
            }
        ],
    }


class FixtureOutputValidationTest(unittest.TestCase):
    def test_rejects_all_empty_output(self):
        result = fixture_result([], [])

        with self.assertRaisesRegex(update_fixtures.ScrapeError, "no fixtures"):
            update_fixtures.validate_fixture_output(result)

    def test_rejects_partially_empty_grades_by_default(self):
        result = fixture_result([{"date": "2026-05-18"}], [])

        with self.assertRaisesRegex(update_fixtures.ScrapeError, "Grade 2"):
            update_fixtures.validate_fixture_output(result)

    def test_can_allow_partially_empty_grades(self):
        result = fixture_result([{"date": "2026-05-18"}], [])

        update_fixtures.validate_fixture_output(result, allow_empty_grades=True)

    def test_fetch_failure_aborts_scrape(self):
        with patch.object(update_fixtures, "fetch_soup", side_effect=RuntimeError("network down")):
            with self.assertRaisesRegex(update_fixtures.ScrapeError, "network down"):
                update_fixtures.parse_team_page("https://example.invalid/team", "Premier League")


if __name__ == "__main__":
    unittest.main()
