import json
from pathlib import Path


BENCHMARK_PATH = Path("evaluation_benchmark.json")
MAX_RANK = 5


def load_benchmark():
    if not BENCHMARK_PATH.exists():
        raise FileNotFoundError(
            "evaluation_benchmark.json was not found. "
            "Run generate_benchmark.py first."
        )

    with open(
        BENCHMARK_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_benchmark(benchmark):
    with open(
        BENCHMARK_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            benchmark,
            file,
            indent=2,
            ensure_ascii=False,
        )


def get_label():
    while True:
        answer = input(
            "\nRelevant? "
            "[Y] Yes  [N] No  [S] Skip  [Q] Quit: "
        ).strip().lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        if answer == "s":
            return "skip"

        if answer == "q":
            return "quit"

        print("⚠️ Please enter Y, N, S, or Q.")


def main():
    benchmark = load_benchmark()

    print("\n🏷️ MANUAL RELEVANCE LABELING")
    print("=" * 60)

    print(
        "\nOnly Top 5 results per query will be labeled."
    )

    print(
        "Label a chunk as relevant only if it "
        "directly helps answer the query."
    )

    # Count only unlabeled Top-5 results
    total_unlabeled = sum(
        1
        for test in benchmark
        for result in test["results"]
        if (
            result["rank"] <= MAX_RANK
            and result["relevant"] is None
        )
    )

    print(
        f"\nTop-5 results remaining: "
        f"{total_unlabeled}"
    )

    completed = 0

    for test in benchmark:
        query = test["query"]

        for result in test["results"]:

            # Ignore Rank 6+
            if result["rank"] > MAX_RANK:
                continue

            # Preserve previous labels
            if result["relevant"] is not None:
                continue

            print("\n" + "=" * 60)
            print(f"🔎 QUERY: {query}")
            print("=" * 60)

            print(f"\n📍 Rank: {result['rank']}")
            print(f"📰 Title: {result['title']}")
            print(f"🏢 Source: {result['source']}")

            print("\n📄 Evidence chunk:\n")
            print(result["text"])

            print("\n" + "-" * 60)

            label = get_label()

            if label == "quit":
                save_benchmark(benchmark)

                print("\n💾 Progress saved.")
                print(
                    f"Remaining Top-5 results: "
                    f"{total_unlabeled - completed}"
                )
                return

            if label == "skip":
                continue

            result["relevant"] = label
            completed += 1

            # Save after every judgment
            save_benchmark(benchmark)

            print(
                f"✅ Saved "
                f"({completed}/{total_unlabeled})"
            )

    save_benchmark(benchmark)

    print("\n" + "=" * 60)
    print("🎉 TOP-5 LABELING COMPLETE")
    print("=" * 60)
    print("All benchmark Top-5 results are labeled.")


if __name__ == "__main__":
    main()