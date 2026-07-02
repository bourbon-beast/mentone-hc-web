import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class NewsDataTests(unittest.TestCase):
    def test_news_json_is_valid(self):
        with (ROOT / "news.json").open(encoding="utf-8") as fh:
            data = json.load(fh)

        self.assertIsInstance(data.get("articles"), list)
        self.assertGreater(len(data["articles"]), 0)

    def test_news_filters_are_apostrophe_safe(self):
        html = (ROOT / "news.html").read_text(encoding="utf-8")

        self.assertIn('data-category="${c}"', html)
        self.assertNotIn("onclick=\"filterNews('${c}')\"", html)


if __name__ == "__main__":
    unittest.main()
