import json
import math
from pathlib import Path


BENCHMARK_PATH = Path("evaluation_benchmark.json")
K = 5


def precision_at_k(labels, k=5):
    top_k = labels[:k]

    if not top_k:
        return 0.0

    return sum(top_k) / len(top_k)


def reciprocal_rank(labels):
    for rank, relevant in enumerate(labels, start=1):
        if relevant:
            return 1.0 / rank

    return 0.0


def ndcg_at_k(labels, k=5):
    top_k = labels[:k]

    dcg = sum(
        relevant / math.log2(index + 2)
        for index, relevant in enumerate(top_k)
    )

    ideal = sorted(top_k, reverse=True)

    idcg = sum(
        relevant / math.log2(index + 2)
        for index, relevant in enumerate(ideal)
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg


def main():
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(
            "evaluation_benchmark.json was not found."
        )

    with open(
        BENCHMARK_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        benchmark = json.load(file)

    precision_scores = []
    rr_scores = []
    ndcg_scores = []

    print("\n📊 HUMAN-LABELED RETRIEVAL EVALUATION")
    print("=" * 60)

    for test in benchmark:
        query = test["query"]

        # Only evaluate manually labeled Top-5 results
        results = [
            result
            for result in test["results"]
            if (
                result["rank"] <= K
                and result["relevant"] is not None
            )
        ]

        results.sort(
            key=lambda result: result["rank"]
        )

        labels = [
            1 if result["relevant"] else 0
            for result in results
        ]

        if len(labels) < K:
            print(
                f"\n⚠️ Skipping '{query}' — "
                f"only {len(labels)}/{K} Top-5 results labeled."
            )
            continue

        precision = precision_at_k(labels, K)
        rr = reciprocal_rank(labels)
        ndcg = ndcg_at_k(labels, K)

        precision_scores.append(precision)
        rr_scores.append(rr)
        ndcg_scores.append(ndcg)

        print(f"\n🔎 {query}")
        print("-" * 60)

        print(
            "Labels:      "
            + " ".join(
                "✅" if label else "❌"
                for label in labels
            )
        )

        print(f"Precision@5: {precision:.3f}")
        print(f"RR:          {rr:.3f}")
        print(f"nDCG@5:      {ndcg:.3f}")

    print("\n" + "=" * 60)
    print("📈 OVERALL RESULTS")
    print("=" * 60)

    if not precision_scores:
        print("No fully labeled queries available.")
        return

    query_count = len(precision_scores)

    mean_precision = (
        sum(precision_scores) / query_count
    )

    mrr = (
        sum(rr_scores) / query_count
    )

    mean_ndcg = (
        sum(ndcg_scores) / query_count
    )

    print(
        f"Mean Precision@5: {mean_precision:.3f}"
    )

    print(
        f"MRR:              {mrr:.3f}"
    )

    print(
        f"Mean nDCG@5:      {mean_ndcg:.3f}"
    )

    print(
        f"Queries evaluated: {query_count}"
    )


if __name__ == "__main__":
    main()