import json
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]


class FixtureDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (REPO_ROOT / "fixtures.json").open(encoding="utf-8") as fh:
            cls.data = json.load(fh)

    def test_all_configured_grades_have_fixtures(self):
        empty_grades = [
            f"{section['label']} / {grade['grade']}"
            for section in self.data["sections"]
            for grade in section["grades"]
            if not grade["fixtures"]
        ]

        self.assertEqual(empty_grades, [])

    def test_no_fixture_lists_mentone_as_its_own_opponent(self):
        self_opponents = [
            f"{section['label']} / {grade['grade']} / {fixture['date']}"
            for section in self.data["sections"]
            for grade in section["grades"]
            for fixture in grade["fixtures"]
            if fixture.get("opponent") == "Mentone Hockey Club"
        ]

        self.assertEqual(self_opponents, [])

    def test_fixture_result_values_match_page_contract(self):
        bad_results = [
            f"{section['label']} / {grade['grade']} / {fixture['date']}: {fixture.get('result')}"
            for section in self.data["sections"]
            for grade in section["grades"]
            for fixture in grade["fixtures"]
            if fixture.get("result") not in {None, "W", "L", "D"}
        ]

        self.assertEqual(bad_results, [])


if __name__ == "__main__":
    unittest.main()
