import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(name):
    with (ROOT / name).open(encoding="utf-8") as content_file:
        return json.load(content_file)


def test_news_feed_shape():
    news = load_json("news.json")

    assert isinstance(news.get("updated"), str)
    articles = news.get("articles")
    assert isinstance(articles, list)
    assert articles

    seen_ids = set()
    for article in articles:
        article_id = article.get("id")
        assert isinstance(article_id, str)
        assert article_id not in seen_ids
        seen_ids.add(article_id)

        for field in ("date", "category", "title", "excerpt", "body", "image"):
            assert isinstance(article.get(field), str)
            assert article[field]

        assert isinstance(article.get("featured"), bool)


def test_fixtures_feed_shape():
    fixtures = load_json("fixtures.json")

    assert isinstance(fixtures.get("updated"), str)
    sections = fixtures.get("sections")
    assert isinstance(sections, list)
    assert sections

    for section in sections:
        for field in ("id", "label", "color"):
            assert isinstance(section.get(field), str)
            assert section[field]

        grades = section.get("grades")
        assert isinstance(grades, list)
        assert grades

        for grade in grades:
            assert isinstance(grade.get("grade"), str)
            assert grade["grade"]

            grade_fixtures = grade.get("fixtures")
            assert isinstance(grade_fixtures, list)
            assert grade_fixtures

            for fixture in grade_fixtures:
                for field in ("date", "day", "time", "opponent", "venue"):
                    assert isinstance(fixture.get(field), str)
                    assert fixture[field]


if __name__ == "__main__":
    test_news_feed_shape()
    test_fixtures_feed_shape()
