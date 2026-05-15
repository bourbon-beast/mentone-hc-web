import importlib
import importlib.util
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

if importlib.util.find_spec("bs4") is None:
    bs4_stub = types.ModuleType("bs4")
    bs4_stub.BeautifulSoup = object
    sys.modules["bs4"] = bs4_stub

if importlib.util.find_spec("requests") is None:
    requests_stub = types.ModuleType("requests")
    sys.modules["requests"] = requests_stub

update_fixtures = importlib.import_module("scripts.update_fixtures")


def fixtures_doc(counts):
    return {
        "updated": "2026-05-15",
        "sections": [
            {
                "id": "mens",
                "label": "Men's",
                "color": "yellow",
                "grades": [
                    {"grade": grade, "fixtures": [{} for _ in range(count)]}
                    for grade, count in counts
                ],
            }
        ],
    }


class UpdateFixturesTests(unittest.TestCase):
    def test_parse_team_page_fails_when_fetch_fails(self):
        with patch.object(update_fixtures, "fetch_soup", side_effect=OSError("offline")):
            with self.assertRaises(update_fixtures.FixtureUpdateError) as ctx:
                update_fixtures.parse_team_page("https://example.test/team", "Premier League")

        self.assertIn("could not fetch Premier League fixtures", str(ctx.exception))

    def test_validation_rejects_zero_fixture_output(self):
        result = fixtures_doc([("Premier League", 0), ("PLR", 0)])

        with self.assertRaises(update_fixtures.FixtureUpdateError) as ctx:
            update_fixtures.validate_scraped_fixtures(result)

        self.assertIn("zero fixtures", str(ctx.exception))

    def test_validation_rejects_grade_that_would_be_wiped(self):
        existing = fixtures_doc([("Premier League", 4), ("PLR", 3)])
        result = fixtures_doc([("Premier League", 0), ("PLR", 3)])

        with self.assertRaises(update_fixtures.FixtureUpdateError) as ctx:
            update_fixtures.validate_scraped_fixtures(result, existing)

        self.assertIn("Men's / Premier League", str(ctx.exception))

    def test_validation_rejects_large_truncation(self):
        existing = fixtures_doc([("Premier League", 10), ("PLR", 8)])
        result = fixtures_doc([("Premier League", 4), ("PLR", 4)])

        with self.assertRaises(update_fixtures.FixtureUpdateError) as ctx:
            update_fixtures.validate_scraped_fixtures(result, existing)

        self.assertIn("less than half", str(ctx.exception))

    def test_validation_accepts_non_destructive_update(self):
        existing = fixtures_doc([("Premier League", 4), ("PLR", 3)])
        result = fixtures_doc([("Premier League", 3), ("PLR", 2)])

        update_fixtures.validate_scraped_fixtures(result, existing)


if __name__ == "__main__":
    unittest.main()
