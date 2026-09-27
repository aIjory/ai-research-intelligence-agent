from collector import (
    calculate_relevance,
    normalize_text,
)


def test_normalize_text():
    result = normalize_text(
        "Autonomous Coding-Assistants!"
    )

    assert result == "autonomous coding assistants "


def test_exact_topic_in_title_scores_highly():
    score = calculate_relevance(
        topic="autonomous coding assistants",
        title="Autonomous Coding Assistants",
        summary="A new generation of developer tools.",
    )

    assert score > 0


def test_unrelated_article_scores_zero():
    score = calculate_relevance(
        topic="autonomous coding assistants",
        title="Weather Forecast",
        summary="Rain is expected tomorrow.",
    )

    assert score == 0