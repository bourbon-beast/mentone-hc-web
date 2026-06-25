import json
from collections import Counter
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FixturesDataTests(unittest.TestCase):
    def load_fixtures(self):
        with (ROOT / "fixtures.json").open(encoding="utf-8") as fh:
            return json.load(fh)

    def test_committed_fixtures_have_no_empty_grades(self):
        data = self.load_fixtures()
        empty = [
            (section["id"], grade["grade"])
            for section in data["sections"]
            for grade in section["grades"]
            if not grade["fixtures"]
        ]

        self.assertEqual(empty, [])

    def test_committed_fixtures_have_no_duplicate_matches_per_grade(self):
        data = self.load_fixtures()
        duplicates = []
        for section in data["sections"]:
            for grade in section["grades"]:
                keys = [
                    (
                        fixture.get("date"),
                        fixture.get("time"),
                        fixture.get("opponent"),
                        fixture.get("venue"),
                        fixture.get("result"),
                    )
                    for fixture in grade["fixtures"]
                ]
                duplicates.extend(
                    (section["id"], grade["grade"], key, count)
                    for key, count in Counter(keys).items()
                    if count > 1
                )

        self.assertEqual(duplicates, [])

    def test_result_cell_handles_scraper_result_letters(self):
        html = (ROOT / "fixtures.html").read_text(encoding="utf-8")

        self.assertIn("if (result === 'W')", html)
        self.assertIn("fix-result win", html)
        self.assertIn("if (result === 'L')", html)
        self.assertIn("fix-result loss", html)
        self.assertIn("if (result === 'D')", html)
        self.assertIn("fix-result draw", html)


if __name__ == "__main__":
    unittest.main()
