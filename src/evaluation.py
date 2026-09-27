def precision_at_k(retrieved_titles, relevant_keywords, k=5):
    """
    Calculate Precision@K using expected relevance keywords.
    """

    top_results = retrieved_titles[:k]

    if not top_results:
        return 0.0

    relevant_count = 0

    for title in top_results:
        normalized_title = title.lower()

        if any(
            keyword.lower() in normalized_title
            for keyword in relevant_keywords
        ):
            relevant_count += 1

    return relevant_count / len(top_results)


def evaluate_results(
    query,
    evidence,
    relevant_keywords,
    k=5,
):
    """
    Evaluate retrieved RAG evidence.
    """

    titles = [
        item["title"]
        for item in evidence
    ]

    precision = precision_at_k(
        titles,
        relevant_keywords,
        k=k,
    )

    print("\n📊 RETRIEVAL EVALUATION")
    print("-" * 40)

    print(f"Query: {query}")
    print(f"Precision@{k}: {precision:.2f}")

    print("\nTop retrieved sources:")

    for index, item in enumerate(
        evidence[:k],
        start=1,
    ):
        print(
            f"{index}. {item['title']}"
        )

    return precision