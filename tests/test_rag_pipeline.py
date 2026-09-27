from rag_pipeline import apply_source_diversity


def make_result(url, score):
    return {
        "url": url,
        "title": url,
        "source": "Test Source",
        "text": "Test evidence",
        "reranker_score": score,
    }


def test_source_diversity_limits_chunks_per_article():
    results = [
        make_result("article-a", 0.9),
        make_result("article-a", 0.8),
        make_result("article-a", 0.7),
        make_result("article-b", 0.6),
        make_result("article-c", 0.5),
    ]

    selected = apply_source_diversity(
        results,
        top_k=5,
        max_per_source=2,
    )

    urls = [
        result["url"]
        for result in selected
    ]

    assert urls.count("article-a") == 2
    assert "article-b" in urls
    assert "article-c" in urls


def test_source_diversity_respects_top_k():
    results = [
        make_result("article-a", 0.9),
        make_result("article-b", 0.8),
        make_result("article-c", 0.7),
    ]

    selected = apply_source_diversity(
        results,
        top_k=2,
        max_per_source=2,
    )

    assert len(selected) == 2