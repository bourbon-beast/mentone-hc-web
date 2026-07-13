import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DataFeedTests(unittest.TestCase):
    def load_json(self, filename):
        with open(REPO_ROOT / filename, encoding="utf-8") as handle:
            return json.load(handle)

    def test_news_feed_is_valid_and_renderable(self):
        data = self.load_json("news.json")

        self.assertIsInstance(data.get("updated"), str)
        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

        required_fields = {
            "id",
            "date",
            "category",
            "title",
            "excerpt",
            "body",
            "image",
            "featured",
        }
        for article in data["articles"]:
            self.assertTrue(required_fields.issubset(article), article)

    def test_fixtures_feed_is_valid_and_renderable(self):
        data = self.load_json("fixtures.json")

        self.assertIsInstance(data.get("updated"), str)
        self.assertIsInstance(data.get("sections"), list)
        self.assertGreater(len(data["sections"]), 0)

        for section in data["sections"]:
            self.assertIsInstance(section.get("id"), str)
            self.assertIsInstance(section.get("label"), str)
            self.assertIsInstance(section.get("grades"), list)
            self.assertGreater(len(section["grades"]), 0)

            for grade in section["grades"]:
                self.assertIsInstance(grade.get("grade"), str)
                self.assertIsInstance(grade.get("fixtures"), list)
                for fixture in grade["fixtures"]:
                    for field in ("date", "day", "time", "opponent", "venue"):
                        self.assertIn(field, fixture)


if __name__ == "__main__":
    unittest.main()
