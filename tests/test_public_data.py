import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class PublicDataTest(unittest.TestCase):
    def test_news_json_loads_for_news_page(self):
        data = json.loads((ROOT / "news.json").read_text(encoding="utf-8"))

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_fixtures_json_loads_for_fixtures_page(self):
        data = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))

        self.assertIsInstance(data.get("sections"), list)
        self.assertGreater(len(data["sections"]), 0)


if __name__ == "__main__":
    unittest.main()
