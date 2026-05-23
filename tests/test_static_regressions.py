import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StaticRegressionTests(unittest.TestCase):
    def test_news_json_is_valid_and_has_unique_articles(self):
        data = json.loads((ROOT / "news.json").read_text(encoding="utf-8"))

        articles = data.get("articles")
        self.assertIsInstance(articles, list)
        self.assertGreater(len(articles), 0)

        ids = [article["id"] for article in articles]
        self.assertEqual(len(ids), len(set(ids)))

    def test_fixtures_json_is_valid(self):
        data = json.loads((ROOT / "fixtures.json").read_text(encoding="utf-8"))

        self.assertIsInstance(data.get("sections"), list)
        self.assertGreater(len(data["sections"]), 0)

    def test_news_dynamic_controls_do_not_use_fragile_inline_handlers(self):
        html = (ROOT / "news.html").read_text(encoding="utf-8")

        self.assertNotIn('onclick="filterNews(', html)
        self.assertNotIn('onclick="renderNews(', html)
        self.assertIn("data-category=", html)
        self.assertIn("data-news-back", html)
        self.assertIn("contentEl.addEventListener('click'", html)

    def test_fixture_results_handle_scraped_outcome_letters(self):
        html = (ROOT / "fixtures.html").read_text(encoding="utf-8")

        self.assertIn("normalised === 'W'", html)
        self.assertIn("normalised === 'L'", html)
        self.assertIn("normalised === 'D'", html)


if __name__ == "__main__":
    unittest.main()
