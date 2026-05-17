import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]

try:
    import requests  # noqa: F401
except ModuleNotFoundError:
    sys.modules["requests"] = types.SimpleNamespace(get=None)

try:
    import bs4  # noqa: F401
except ModuleNotFoundError:
    sys.modules["bs4"] = types.SimpleNamespace(BeautifulSoup=object)

spec = importlib.util.spec_from_file_location(
    "update_fixtures", ROOT / "scripts" / "update_fixtures.py"
)
update_fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update_fixtures)


def fixture_data(total):
    return {
        "updated": "2026-05-17",
        "sections": [
            {
                "id": "mens",
                "label": "Men's",
                "color": "yellow",
                "grades": [
                    {
                        "grade": "Premier League",
                        "fixtures": [
                            {"date": f"2026-05-{day:02d}"}
                            for day in range(1, total + 1)
                        ],
                    }
                ],
            }
        ],
    }


class UpdateFixturesSafetyTest(unittest.TestCase):
    def test_parse_team_page_fails_closed_when_fetch_fails(self):
        with mock.patch.object(
            update_fixtures, "fetch_soup", side_effect=RuntimeError("network down")
        ):
            with self.assertRaisesRegex(update_fixtures.ScrapeError, "could not fetch"):
                update_fixtures.parse_team_page(
                    "https://example.com/team", "Premier League"
                )

    def test_validate_rejects_zero_fixture_scrape(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "fixtures.json"
            with self.assertRaisesRegex(update_fixtures.ScrapeError, "zero fixtures"):
                update_fixtures.validate_fixture_update(fixture_data(0), output)

    def test_validate_rejects_suspicious_mass_drop(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "fixtures.json"
            output.write_text(json.dumps(fixture_data(10)), encoding="utf-8")

            with self.assertRaisesRegex(update_fixtures.ScrapeError, "10 currently"):
                update_fixtures.validate_fixture_update(fixture_data(4), output)

    def test_validate_allows_comparable_fixture_count(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "fixtures.json"
            output.write_text(json.dumps(fixture_data(10)), encoding="utf-8")

            update_fixtures.validate_fixture_update(fixture_data(5), output)


if __name__ == "__main__":
    unittest.main()
