import feedparser


RSS_FEEDS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
]


def collect_research(topic):
    print(f"\n🌐 Collecting research about: {topic}")

    results = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", "")
            link = entry.get("link", "")

            content = f"{title} {summary}".lower()

            if topic.lower() in content:
                results.append({
                    "title": title,
                    "summary": summary,
                    "url": link
                })

    return results