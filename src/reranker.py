from sentence_transformers import CrossEncoder


reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


def rerank_articles(topic, articles, top_k=15):
    """
    Rerank candidate articles using a cross-encoder.

    Unlike embedding similarity, the cross-encoder
    evaluates the query and article together.
    """

    if not articles:
        return []

    pairs = []

    for article in articles:
        article_text = (
            f"{article['title']}. "
            f"{article['summary']}"
        )

        pairs.append(
            [topic, article_text]
        )

    scores = reranker.predict(pairs)

    reranked = []

    for article, score in zip(articles, scores):
        article_copy = article.copy()
        article_copy["reranker_score"] = float(score)
        reranked.append(article_copy)

    reranked.sort(
        key=lambda article: article["reranker_score"],
        reverse=True,
    )

    return reranked[:top_k]