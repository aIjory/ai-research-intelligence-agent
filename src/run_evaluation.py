from collector import collect_research
from rag_pipeline import build_rag_context
from evaluation import evaluate_results
from evaluation_dataset import EVALUATION_DATASET


def main():
    scores = []

    print("\n🧪 RAG RETRIEVAL EVALUATION")
    print("=" * 50)

    for test in EVALUATION_DATASET:
        query = test["query"]

        print("\n" + "=" * 50)
        print(f"🔎 Evaluating: {query}")
        print("=" * 50)

        articles = collect_research(
            query,
            max_results=10,
        )

        if not articles:
            print("⚠️ No articles retrieved.")
            scores.append(0.0)
            continue

        evidence = build_rag_context(
            query,
            articles,
            max_articles=5,
            top_k=8,
        )

        if not evidence:
            print("⚠️ No evidence retrieved.")
            scores.append(0.0)
            continue

        precision = evaluate_results(
            query=query,
            evidence=evidence,
            relevant_keywords=test[
                "relevant_keywords"
            ],
            k=5,
        )

        scores.append(precision)

    print("\n" + "=" * 50)
    print("📈 FINAL EVALUATION")
    print("=" * 50)

    if scores:
        average_precision = (
            sum(scores) / len(scores)
        )

        print(
            f"Mean Precision@5: "
            f"{average_precision:.2f}"
        )

        print(
            f"Queries evaluated: "
            f"{len(scores)}"
        )

    else:
        print("No queries were evaluated.")


if __name__ == "__main__":
    main()