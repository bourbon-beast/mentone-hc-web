import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from scripts import update_fixtures


def soup_from(body):
    return BeautifulSoup(body, "html.parser")


class UpdateFixturesTests(unittest.TestCase):
    def test_expected_title_mismatch_is_fatal(self):
        soup = soup_from("<html><body>2026 Senior Competition Other Club</body></html>")

        with self.assertRaises(update_fixtures.FixtureSourceError):
            update_fixtures.validate_expected_title(
                soup,
                "2026 Senior Competition \u00b7 Mens Premier League - 2026 Mentone Hockey Club",
                "Premier League",
            )

    def test_empty_fixture_page_is_fatal(self):
        body = """
        <html><body>
          2026 Senior Competition \u00b7 Mens Premier League - 2026 Mentone Hockey Club
        </body></html>
        """

        with patch.object(update_fixtures, "fetch_soup", return_value=soup_from(body)):
            with self.assertRaises(update_fixtures.FixtureSourceError):
                update_fixtures.parse_team_page(
                    "https://example.test/team",
                    "Premier League",
                    "2026 Senior Competition \u00b7 Mens Premier League - 2026 Mentone Hockey Club",
                )

    def test_bye_placeholder_does_not_duplicate_previous_match(self):
        body = """
        <html><body>
          2026 Senior Competition \u00b7 Mens Premier League - 2026 Mentone Hockey Club
          <div class="draw">
            <div class="match">
              <b>Round 1</b>
              <span>Sat 11 Apr 2026 13:00 Played Win</span>
              <a href="/venues/1">Mentone Hockey Centre</a>
              <a href="/games/team/25879/1">Mens Premier League - 2026 Doncaster Hockey Club</a>
            </div>
            <div class="bye">
              <b>Round 2</b>
              <span>BYE</span>
            </div>
          </div>
        </body></html>
        """

        with patch.object(update_fixtures, "fetch_soup", return_value=soup_from(body)):
            fixtures = update_fixtures.parse_team_page(
                "https://example.test/team",
                "Premier League",
                "2026 Senior Competition \u00b7 Mens Premier League - 2026 Mentone Hockey Club",
            )

        self.assertEqual(
            fixtures,
            [
                {
                    "date": "2026-04-11",
                    "day": "Sat",
                    "time": "1:00pm",
                    "opponent": "Doncaster Hockey Club",
                    "venue": "Home",
                    "result": "W",
                }
            ],
        )

    def test_midweek_competition_prefix_is_removed_from_opponent(self):
        raw = "2026 Midweek Men's 40+ BSE Doncaster Hockey Club"

        self.assertEqual(
            update_fixtures.clean_opponent(raw),
            "Doncaster Hockey Club",
        )


if __name__ == "__main__":
    unittest.main()
