import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class PublicDataJsonTest(unittest.TestCase):
    def test_news_json_is_valid_and_has_articles(self):
        data = json.loads((REPO_ROOT / "news.json").read_text(encoding="utf-8"))

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_fixtures_json_is_valid_and_has_fixtures(self):
        data = json.loads((REPO_ROOT / "fixtures.json").read_text(encoding="utf-8"))
        total_fixtures = sum(
            len(grade.get("fixtures", []))
            for section in data.get("sections", [])
            for grade in section.get("grades", [])
        )

        self.assertGreater(total_fixtures, 0)


if __name__ == "__main__":
    unittest.main()
