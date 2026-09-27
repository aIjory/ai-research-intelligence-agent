from datetime import datetime, timedelta, timezone

from hybrid_ranker import (
    calculate_keyword_score,
    calculate_recency_score,
    rank_articles_hybrid,
)


def test_keyword_score_normalization():
    assert calculate_keyword_score(0) == 0.0
    assert calculate_keyword_score(5) == 0.5
    assert calculate_keyword_score(10) == 1.0
    assert calculate_keyword_score(20) == 1.0


def test_recent_article_gets_highest_recency():
    published = datetime.now(timezone.utc) - timedelta(days=5)

    assert calculate_recency_score(published) == 1.0


def test_old_article_gets_zero_recency():
    published = datetime.now(timezone.utc) - timedelta(days=500)

    assert calculate_recency_score(published) == 0.0


def test_missing_date_gets_default_recency():
    assert calculate_recency_score(None) == 0.3


def test_hybrid_ranking_orders_by_final_score():
    now = datetime.now(timezone.utc)

    articles = [
        {
            "title": "Lower relevance",
            "semantic_score": 0.40,
            "relevance_score": 1,
            "published_date": now,
        },
        {
            "title": "Higher relevance",
            "semantic_score": 0.80,
            "relevance_score": 8,
            "published_date": now,
        },
    ]

    ranked = rank_articles_hybrid(articles)

    assert ranked[0]["title"] == "Higher relevance"
    assert ranked[0]["final_score"] > ranked[1]["final_score"]

    assert "keyword_score" in ranked[0]
    assert "recency_score" in ranked[0]
    assert "final_score" in ranked[0]