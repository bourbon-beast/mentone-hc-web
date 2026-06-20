import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class NewsDataTests(unittest.TestCase):
    def test_news_json_is_valid_and_has_articles(self):
        with (ROOT / "news.json").open(encoding="utf-8") as fh:
            data = json.load(fh)

        self.assertIn("updated", data)
        self.assertGreater(len(data.get("articles", [])), 0)

    def test_news_article_ids_are_unique(self):
        with (ROOT / "news.json").open(encoding="utf-8") as fh:
            data = json.load(fh)

        ids = [article["id"] for article in data["articles"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_news_filters_do_not_use_apostrophe_broken_inline_js(self):
        html = (ROOT / "news.html").read_text(encoding="utf-8")

        self.assertNotIn("onclick=\"filterNews('${c}')\"", html)
        self.assertIn('data-category="${c}"', html)
        self.assertIn("addEventListener('click'", html)


if __name__ == "__main__":
    unittest.main()
