import json

from collector import collect_research
from rag_pipeline import build_rag_context
from evaluation_dataset import EVALUATION_DATASET


def main():
    benchmark = []

    print("\n🧪 GENERATING MANUAL RELEVANCE BENCHMARK")
    print("=" * 60)

    for test in EVALUATION_DATASET:
        query = test["query"]

        print("\n" + "=" * 60)
        print(f"🔎 Query: {query}")
        print("=" * 60)

        articles = collect_research(
            query,
            max_results=10,
        )

        if not articles:
            print("⚠️ No articles retrieved.")
            continue

        evidence = build_rag_context(
            query,
            articles,
            max_articles=5,
            top_k=8,
        )

        results = []

        for rank, item in enumerate(
            evidence,
            start=1,
        ):
            result = {
                "rank": rank,
                "title": item["title"],
                "source": item["source"],
                "url": item["url"],
                "text": item["text"],
                "vector_score": item.get(
                    "vector_score"
                ),
                "reranker_score": item.get(
                    "reranker_score"
                ),
                "relevant": None,
            }

            results.append(result)

        benchmark.append(
            {
                "query": query,
                "results": results,
            }
        )

    output_path = "evaluation_benchmark.json"

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            benchmark,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 60)
    print("✅ BENCHMARK GENERATED")
    print("=" * 60)
    print(f"Saved to: {output_path}")
    print(
        "\nNext step: manually label each result "
        "as relevant or not relevant."
    )


if __name__ == "__main__":
    main()