import re
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime

import feedparser

from semantic_ranker import rank_articles_semantically
from hybrid_ranker import rank_articles_hybrid
from reranker import rerank_articles


RSS_FEEDS = [
    {
        "name": "TechCrunch AI",
        "url": "https://techcrunch.com/category/artificial-intelligence/feed/",
    },
    {
        "name": "Google AI",
        "url": "https://blog.google/technology/ai/rss/",
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co/blog/feed.xml",
    },
]


def normalize_text(text):
    """Normalize text for keyword matching."""

    return re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text.lower(),
    )


def calculate_relevance(topic, title, summary):
    """Calculate basic keyword relevance."""

    normalized_topic = normalize_text(topic)
    normalized_title = normalize_text(title)
    normalized_summary = normalize_text(summary)

    topic_words = normalized_topic.split()
    title_words = normalized_title.split()
    summary_words = normalized_summary.split()

    score = 0

    for word in topic_words:
        if word in title_words:
            score += 3

        if word in summary_words:
            score += 1

    if normalized_topic in normalized_title:
        score += 5

    return score


def parse_date(entry):
    """Convert an RSS publication date into a datetime."""

    published = entry.get("published", "")

    if not published:
        return None

    try:
        date = parsedate_to_datetime(published)

        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)

        return date

    except (TypeError, ValueError):
        return None


def collect_research(topic, max_results=15):
    """
    Collect and rank recent articles using:
    - recency filtering
    - semantic retrieval
    - hybrid scoring
    - cross-encoder reranking
    """

    print(f"\n🌐 Collecting research about: {topic}")

    results = []
    seen_urls = set()

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=365)

    # ------------------------------------------------
    # 1. Collect articles
    # ------------------------------------------------

    for source in RSS_FEEDS:

        print(f"   Checking {source['name']}...")

        try:
            feed = feedparser.parse(source["url"])

        except Exception as error:
            print(
                f"   ⚠️ Could not load {source['name']}: {error}"
            )
            continue

        if getattr(feed, "bozo", False) and not feed.entries:
            print(
                f"   ⚠️ Invalid or unavailable feed: "
                f"{source['name']}"
            )
            continue

        for entry in feed.entries:

            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            published = entry.get(
                "published",
                "Unknown date",
            )

            if not link:
                continue

            if link in seen_urls:
                continue

            published_date = parse_date(entry)

            # Skip articles older than 12 months
            if (
                published_date is not None
                and published_date < cutoff_date
            ):
                continue

            relevance_score = calculate_relevance(
                topic,
                title,
                summary,
            )

            article = {
                "title": title,
                "summary": summary,
                "url": link,
                "source": source["name"],
                "published": published,
                "published_date": published_date,
                "relevance_score": relevance_score,
            }

            results.append(article)
            seen_urls.add(link)

    print(
        f"   Collected {len(results)} unique recent articles."
    )

    # ------------------------------------------------
    # 2. Stop if nothing was collected
    # ------------------------------------------------

    if not results:
        print("   ⚠️ No recent articles were available.")
        return []

    # ------------------------------------------------
    # 3. Candidate pre-ranking
    # ------------------------------------------------

    results.sort(
        key=lambda article: (
            article["relevance_score"],
            article["published_date"]
            or datetime.min.replace(tzinfo=timezone.utc),
        ),
        reverse=True,
    )

    candidate_articles = results[:100]

    print(
        f"   Semantic ranking "
        f"{len(candidate_articles)} candidate articles..."
    )

    # ------------------------------------------------
    # 4. Semantic ranking
    # ------------------------------------------------

    semantic_articles = rank_articles_semantically(
        topic,
        candidate_articles,
        top_k=50,
    )

    # ------------------------------------------------
    # 5. Semantic threshold
    # ------------------------------------------------

    semantic_articles = [
        article
        for article in semantic_articles
        if article["semantic_score"] >= 0.35
    ]

    print(
        f"   {len(semantic_articles)} articles passed "
        f"the semantic relevance threshold."
    )

    if not semantic_articles:
        print(
            "   ⚠️ No articles passed the semantic "
            "relevance threshold."
        )
        return []

    # ------------------------------------------------
    # 6. Hybrid ranking
    # ------------------------------------------------

    hybrid_articles = rank_articles_hybrid(
        semantic_articles
    )

    print(
        f"   Hybrid ranking produced "
        f"{len(hybrid_articles)} candidates."
    )

    # ------------------------------------------------
    # 7. Cross-encoder reranking
    # ------------------------------------------------

    print(
        f"   Cross-encoder reranking "
        f"{len(hybrid_articles)} candidates..."
    )

    reranked_articles = rerank_articles(
        topic,
        hybrid_articles,
        top_k=max_results,
    )

    print(
        f"   Selected {len(reranked_articles)} "
        f"articles after cross-encoder reranking."
    )

    return reranked_articles