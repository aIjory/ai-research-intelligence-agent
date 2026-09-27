from collector import collect_research
from rag_pipeline import build_rag_context
from rag_analyzer import analyze_rag_evidence
from reporter import save_report


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    topic = input(
        "What topic would you like to research? "
    ).strip()

    if not topic:
        print("\n⚠️ Please enter a research topic.")
        return

    print(f"\n🔎 Research topic: {topic}")

    # ------------------------------------------------
    # 1. Collect and rank relevant articles
    # ------------------------------------------------

    sources = collect_research(topic)

    print(f"\n📚 Sources collected: {len(sources)}")

    if not sources:
        print("\n⚠️ No relevant sources were found.")
        return

    # ------------------------------------------------
    # 2. Display ranked articles and ranking scores
    # ------------------------------------------------

    for source in sources:

        print(f"\n📰 {source['title']}")

        print(
            f"🏢 Source: "
            f"{source['source']}"
        )

        print(
            f"📅 Published: "
            f"{source['published']}"
        )

        print(
            f"🔗 {source['url']}"
        )

        print(
            f"📊 Scores: "
            f"semantic="
            f"{source.get('semantic_score', 0):.3f} | "
            f"keyword="
            f"{source.get('keyword_score', 0):.3f} | "
            f"recency="
            f"{source.get('recency_score', 0):.3f} | "
            f"hybrid="
            f"{source.get('final_score', 0):.3f} | "
            f"reranker="
            f"{source.get('reranker_score', 0):.3f}"
        )

    # ------------------------------------------------
    # 3. Build RAG knowledge base
    # ------------------------------------------------

    evidence = build_rag_context(
        topic,
        sources,
        max_articles=5,
        top_k=8,
    )

    if not evidence:
        print(
            "\n⚠️ No sufficiently relevant evidence "
            "could be retrieved."
        )
        return

    print(
        f"\n🔍 Retrieved {len(evidence)} "
        f"evidence chunks."
    )

    # ------------------------------------------------
    # 4. Display retrieved evidence scores
    # ------------------------------------------------

    print("\n📖 Retrieved evidence:")

    for index, item in enumerate(
        evidence,
        start=1,
    ):
        print(
            f"\nEvidence {index}"
        )

        print(
            f"🏢 Source: "
            f"{item['source']}"
        )

        print(
            f"📰 Title: "
            f"{item['title']}"
        )

        print(
            f"🎯 Similarity: "
            f"{item['score']:.3f}"
        )

    # ------------------------------------------------
    # 5. Analyze retrieved evidence
    # ------------------------------------------------

    print(
        "\n🧠 Analyzing retrieved evidence "
        "with AI..."
    )

    analysis = analyze_rag_evidence(
        topic,
        evidence,
    )

    # ------------------------------------------------
    # 6. Display structured intelligence brief
    # ------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "RAG-GROUNDED STRATEGIC "
        "INTELLIGENCE BRIEF"
    )

    print("=" * 60)

    print("\n📌 RAW FACTS")

    for fact in analysis.raw_facts:
        print(f"• {fact}")

    print(
        "\n💡 STRATEGIC INTERPRETATION"
    )

    for insight in (
        analysis.strategic_interpretation
    ):
        print(f"• {insight}")

    print("\n🎯 CONFIDENCE")

    print(
        f"Level: "
        f"{analysis.confidence.level}"
    )

    print(
        f"Reason: "
        f"{analysis.confidence.reason}"
    )

    # ------------------------------------------------
    # 7. Save Markdown report
    # ------------------------------------------------

    report_path = save_report(
        topic,
        analysis,
        sources,
    )

    print(
        f"\n💾 Report saved to: "
        f"{report_path}"
    )


if __name__ == "__main__":
    main()