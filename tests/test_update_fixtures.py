import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from scripts.update_fixtures import (
    FixtureSourceError,
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


if __name__ == "__main__":
    unittest.main()
