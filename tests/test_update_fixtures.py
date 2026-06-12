import unittest
from unittest import mock

from scripts import update_fixtures


class UpdateFixturesTests(unittest.TestCase):
    def test_fetch_failures_abort_team_parse(self):
        with mock.patch.object(update_fixtures, "fetch_soup", side_effect=RuntimeError("timeout")):
            with self.assertRaisesRegex(RuntimeError, "timeout"):
                update_fixtures.parse_team_page("https://example.invalid/team", "Premier League")

    def test_rejects_catastrophic_empty_scrape(self):
        config = {
            "sections": [
                {
                    "grades": [
                        {"grade": "Premier League"},
                        {"grade": "PLR"},
                    ]
                }
            ]
        }
        fixtures_data = {
            "sections": [
                {
                    "grades": [
                        {"grade": "Premier League", "fixtures": []},
                        {"grade": "PLR", "fixtures": []},
                    ]
                }
            ]
        }

        with self.assertRaisesRegex(RuntimeError, "0 fixtures across 2 configured grades"):
            update_fixtures.validate_fixture_output(fixtures_data, config)

    def test_allows_some_empty_grades_when_scrape_has_data(self):
        config = {
            "sections": [
                {
                    "grades": [
                        {"grade": "Premier League"},
                        {"grade": "U12 Mixed"},
                    ]
                }
            ]
        }
        fixtures_data = {
            "sections": [
                {
                    "grades": [
                        {"grade": "Premier League", "fixtures": [{"date": "2026-05-23"}]},
                        {"grade": "U12 Mixed", "fixtures": []},
                    ]
                }
            ]
        }

        update_fixtures.validate_fixture_output(fixtures_data, config)


if __name__ == "__main__":
    unittest.main()
