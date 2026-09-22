import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser


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
    """Normalize text for easier keyword matching."""
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())


def calculate_relevance(topic, title, summary):
    """Calculate a simple relevance score for an article."""

    topic = normalize_text(topic)
    title = normalize_text(title)
    summary = normalize_text(summary)

    topic_words = topic.split()

    score = 0

    for word in topic_words:
        # Title matches are more important
        if word in title.split():
            score += 3

        # Summary matches
        if word in summary.split():
            score += 1

    # Bonus if the full topic appears in the title
    if topic in title:
        score += 5

    return score


def parse_date(entry):
    """Convert RSS publication date into a Python datetime."""

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
    """Collect and rank relevant research articles."""

    print(f"\n🌐 Collecting research about: {topic}")

    results = []
    seen_urls = set()

    for source in RSS_FEEDS:
        print(f"   Checking {source['name']}...")

        feed = feedparser.parse(source["url"])

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")
            published = entry.get("published", "Unknown date")

            # Skip duplicate or missing URLs
            if not link or link in seen_urls:
                continue

            relevance_score = calculate_relevance(
                topic,
                title,
                summary,
            )

            # Ignore irrelevant articles
            if relevance_score == 0:
                continue

            published_date = parse_date(entry)

            results.append(
                {
                    "title": title,
                    "summary": summary,
                    "url": link,
                    "source": source["name"],
                    "published": published,
                    "published_date": published_date,
                    "relevance_score": relevance_score,
                }
            )

            seen_urls.add(link)

    # Sort by relevance first, then publication date
    results.sort(
        key=lambda article: (
            article["relevance_score"],
            article["published_date"]
            or datetime.min.replace(tzinfo=timezone.utc),
        ),
        reverse=True,
    )

    return results[:max_results]