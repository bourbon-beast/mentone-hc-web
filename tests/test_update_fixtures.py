import unittest
from unittest import mock

from bs4 import BeautifulSoup

from scripts import update_fixtures


class FixtureScraperValidationTests(unittest.TestCase):
    def test_fetch_soup_rejects_empty_response(self):
        class EmptyResponse:
            text = ""

            def raise_for_status(self):
                return None

        with mock.patch.object(
            update_fixtures.requests,
            "get",
            return_value=EmptyResponse(),
        ):
            with self.assertRaisesRegex(
                update_fixtures.FixtureScrapeError,
                "empty response",
            ):
                update_fixtures.fetch_soup("https://example.com/fixtures")

    def test_parse_team_page_rejects_unexpected_source_title(self):
        soup = BeautifulSoup(
            """
            <html>
              <body>
                <h2>2026 Senior Competition - Mens Metro - 2026 Monash University Hockey Club</h2>
              </body>
            </html>
            """,
            "html.parser",
        )

        with mock.patch.object(update_fixtures, "fetch_soup", return_value=soup):
            with self.assertRaisesRegex(
                update_fixtures.FixtureScrapeError,
                "source title mismatch",
            ):
                update_fixtures.parse_team_page(
                    "https://www.hockeyvictoria.org.au/games/team/25879/412433",
                    "Metro 1 South",
                    "Womens Metro 1 South - 2026 Mentone Hockey Club",
                )

    def test_build_fixtures_json_rejects_empty_grade(self):
        config = {
            "season": 2026,
            "sections": [
                {
                    "id": "womens",
                    "label": "Women's",
                    "color": "blue",
                    "grades": [
                        {
                            "grade": "Premier League",
                            "team_url": "https://example.com/team",
                            "expected_title": "Womens Premier League - 2026 Mentone Hockey Club",
                        }
                    ],
                }
            ],
        }

        with mock.patch.object(update_fixtures, "parse_team_page", return_value=[]):
            with self.assertRaisesRegex(
                update_fixtures.FixtureScrapeError,
                "no fixtures parsed",
            ):
                update_fixtures.build_fixtures_json(config)


if __name__ == "__main__":
    unittest.main()
