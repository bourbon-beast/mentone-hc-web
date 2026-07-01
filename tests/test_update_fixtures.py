import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from scripts.update_fixtures import (
    FixtureSourceError,
    clean_opponent,
    parse_team_page,
    validate_expected_title,
)


class FixtureSourceValidationTests(unittest.TestCase):
    def soup(self, html):
        return BeautifulSoup(html, "html.parser")

    def test_validate_expected_title_accepts_matching_source(self):
        soup = self.soup(
            "<h1>2026 Junior Competition &middot; "
            "U18 Mixed District SE - 2026 Mentone Hockey Club</h1>"
        )

        validate_expected_title(
            soup,
            "2026 Junior Competition · U18 Mixed District SE - 2026 Mentone Hockey Club",
            "U18 Mixed",
        )

    def test_validate_expected_title_rejects_wrong_source(self):
        soup = self.soup(
            "<h1>2026 Senior Competition &middot; "
            "Mens Pennant E South East - 2026 Mornington Peninsula Hockey Club</h1>"
        )

        with self.assertRaises(FixtureSourceError):
            validate_expected_title(
                soup,
                "2026 Junior Competition · U18 Mixed District SE - 2026 Mentone Hockey Club",
                "U18 Mixed",
            )

    def test_parse_team_page_rejects_empty_valid_source(self):
        soup = self.soup(
            "<h1>2026 Junior Competition &middot; "
            "U18 Mixed District SE - 2026 Mentone Hockey Club</h1>"
            "<p>There are no draws to show.</p>"
        )

        with patch("scripts.update_fixtures.fetch_soup", return_value=soup):
            with self.assertRaises(FixtureSourceError):
                parse_team_page(
                    "https://example.test/team",
                    "U18 Mixed",
                    "2026 Junior Competition · U18 Mixed District SE - 2026 Mentone Hockey Club",
                )

    def test_parse_team_page_skips_bye_rounds_without_match_container(self):
        soup = self.soup(
            "<h1>2026 Junior Competition &middot; "
            "U18 Mixed District SE - 2026 Mentone Hockey Club</h1>"
            "<section>"
            "  <div class='match'>"
            "    <b>Round 1</b> Fri 01 May 2026 20:45"
            "    <a href='/venues/1'>Mentone Grammar Playing Fields</a>"
            "    Played"
            "    <a href='/games/team/26323/1'>"
            "      U18 Mixed District SE - 2026 Camberwell Hockey Club"
            "    </a>"
            "    2 - 1 Win"
            "  </div>"
            "  <div class='bye'>"
            "    <b>Round 2</b> Fri 08 May 2026 00:00"
            "    U18 Mixed District SE - 2026 Mentone Hockey Club have a BYE."
            "  </div>"
            "</section>"
        )

        with patch("scripts.update_fixtures.fetch_soup", return_value=soup):
            fixtures = parse_team_page(
                "https://example.test/team",
                "U18 Mixed",
                "2026 Junior Competition · U18 Mixed District SE - 2026 Mentone Hockey Club",
            )

        self.assertEqual(len(fixtures), 1)
        self.assertEqual(fixtures[0]["opponent"], "Camberwell Hockey Club")

    def test_clean_opponent_removes_midweek_prefix(self):
        self.assertEqual(
            clean_opponent("2026 Midweek Women's 35+ A SE Doncaster Hockey Club"),
            "Doncaster Hockey Club",
        )


if __name__ == "__main__":
    unittest.main()
