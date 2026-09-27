from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


# Lightweight embedding model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_articles_semantically(topic, articles, top_k=10):
    """
    Rank articles by semantic similarity to the research topic.
    """

    if not articles:
        return []

    # Create one searchable text representation per article
    article_texts = [
        f"{article['title']} {article['summary']}"
        for article in articles
    ]

    # Convert topic and articles into embeddings
    topic_embedding = model.encode(
        topic,
        convert_to_tensor=True,
    )

    article_embeddings = model.encode(
        article_texts,
        convert_to_tensor=True,
    )

    # Calculate semantic similarity
    similarity_scores = cos_sim(
        topic_embedding,
        article_embeddings,
    )[0]

    # Attach score to each article
    ranked_articles = []

    for article, score in zip(articles, similarity_scores):
        article_copy = article.copy()
        article_copy["semantic_score"] = float(score)
        ranked_articles.append(article_copy)

    # Highest semantic similarity first
    ranked_articles.sort(
        key=lambda article: article["semantic_score"],
        reverse=True,
    )

    return ranked_articles[:top_k]