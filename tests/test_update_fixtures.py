import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from scripts import update_fixtures


class UpdateFixturesSafetyTests(unittest.TestCase):
    def test_fetch_failure_aborts_instead_of_returning_empty_fixtures(self):
        with patch.object(update_fixtures, "fetch_soup", side_effect=RuntimeError("timeout")):
            with self.assertRaisesRegex(update_fixtures.FixtureScrapeError, "could not fetch page"):
                update_fixtures.parse_team_page("https://example.test/team", "Premier League")

    def test_empty_fixture_markup_aborts_instead_of_returning_empty_fixtures(self):
        soup = BeautifulSoup("<html><body><p>No rounds available</p></body></html>", "html.parser")

        with patch.object(update_fixtures, "fetch_soup", return_value=soup):
            with self.assertRaisesRegex(update_fixtures.FixtureScrapeError, "no fixtures found"):
                update_fixtures.parse_team_page("https://example.test/team", "Premier League")


if __name__ == "__main__":
    unittest.main()
