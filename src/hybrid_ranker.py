from datetime import datetime, timezone


def calculate_recency_score(published_date):
    """
    Calculate a recency score between 0 and 1.

    Newer articles receive higher scores.
    """

    if published_date is None:
        return 0.3

    now = datetime.now(timezone.utc)

    age_days = (now - published_date).days

    if age_days <= 30:
        return 1.0

    if age_days <= 90:
        return 0.8

    if age_days <= 180:
        return 0.6

    if age_days <= 365:
        return 0.4

    return 0.0


def calculate_keyword_score(relevance_score):
    """
    Normalize the keyword relevance score
    to a value between 0 and 1.
    """

    return min(relevance_score / 10, 1.0)


def rank_articles_hybrid(articles):
    """
    Combine semantic similarity, keyword relevance,
    and article recency into one ranking score.
    """

    ranked_articles = []

    for article in articles:

        semantic_score = article.get(
            "semantic_score",
            0.0,
        )

        keyword_score = calculate_keyword_score(
            article.get("relevance_score", 0)
        )

        recency_score = calculate_recency_score(
            article.get("published_date")
        )

        # Semantic meaning is the most important signal
        final_score = (
            semantic_score * 0.70
            + keyword_score * 0.25
            + recency_score * 0.05
       )

        article_copy = article.copy()

        article_copy["keyword_score"] = keyword_score
        article_copy["recency_score"] = recency_score
        article_copy["final_score"] = final_score

        ranked_articles.append(article_copy)

    ranked_articles.sort(
        key=lambda article: article["final_score"],
        reverse=True,
    )

    return ranked_articles
