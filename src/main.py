from collector import collect_research
from rag_pipeline import build_rag_context
from rag_analyzer import analyze_rag_evidence
from reporter import save_report


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    # ------------------------------------------------
    # 1. Get research topic
    # ------------------------------------------------

    topic = input(
        "What topic would you like to research? "
    ).strip()

    if not topic:
        print("\n❌ No research topic provided.")
        return

    print(f"\n🔎 Research topic: {topic}")

    # ------------------------------------------------
    # 2. Collect and rank research sources
    # ------------------------------------------------

    sources = collect_research(
        topic,
        max_results=10,
    )

    if not sources:
        print(
            "\n❌ No relevant research sources found."
        )
        return

    print(
        f"\n📚 Sources collected: {len(sources)}"
    )

    # ------------------------------------------------
    # 3. Display ranked sources
    # ------------------------------------------------

    for source in sources:
        print(
            f"\n📰 {source['title']}"
        )
        print(
            f"🏢 Source: {source['source']}"
        )
        print(
            f"📅 Published: {source['published']}"
        )
        print(
            f"🔗 {source['url']}"
        )

        semantic_score = source.get(
            "semantic_score"
        )

        keyword_score = source.get(
            "keyword_score"
        )

        recency_score = source.get(
            "recency_score"
        )

        hybrid_score = source.get(
            "final_score"
        )

        reranker_score = source.get(
            "reranker_score"
        )

        score_parts = []

        if semantic_score is not None:
            score_parts.append(
                f"semantic={semantic_score:.3f}"
            )

        if keyword_score is not None:
            score_parts.append(
                f"keyword={keyword_score:.3f}"
            )

        if recency_score is not None:
            score_parts.append(
                f"recency={recency_score:.3f}"
            )

        if hybrid_score is not None:
            score_parts.append(
                f"hybrid={hybrid_score:.3f}"
            )

        if reranker_score is not None:
            score_parts.append(
                f"reranker={reranker_score:.3f}"
            )

        if score_parts:
            print(
                "📊 Scores: "
                + " | ".join(score_parts)
            )

    # ------------------------------------------------
    # 4. Build RAG evidence
    # ------------------------------------------------

    evidence = build_rag_context(
        topic,
        sources,
    )

    if not evidence:
        print(
            "\n❌ No usable RAG evidence was retrieved."
        )
        return

    print(
        f"\n🔍 Retrieved "
        f"{len(evidence)} evidence chunks."
    )

    # ------------------------------------------------
    # 5. Display retrieved evidence
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
            f"🏢 Source: {item['source']}"
        )
        print(
            f"📰 Title: {item['title']}"
        )

        score = item.get("score")

        if score is not None:
            print(
                f"🎯 Similarity: {score:.3f}"
            )

    # ------------------------------------------------
    # 6. Analyze retrieved evidence
    # ------------------------------------------------

    print(
        "\n🧠 Analyzing retrieved evidence "
        "with AI..."
    )

    try:
        analysis = analyze_rag_evidence(
            topic,
            evidence,
        )

    except ValueError as error:
        print(
            f"\n❌ Analysis failed: {error}"
        )
        return

    # ------------------------------------------------
    # 7. Display strategic intelligence brief
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print(
        "RAG-GROUNDED STRATEGIC INTELLIGENCE BRIEF"
    )
    print("=" * 60)

    # Executive Summary
    print("\n📌 EXECUTIVE SUMMARY")
    print(
        analysis.executive_summary
    )

    # Key Developments
    print("\n🔑 KEY DEVELOPMENTS")

    for index, development in enumerate(
        analysis.key_developments,
        start=1,
    ):
        print(
            f"\n{index}. {development.title}"
        )

        print(
            f"   {development.finding}"
        )

        evidence_refs = ", ".join(
            f"E{evidence_id}"
            for evidence_id
            in development.evidence_ids
        )

        print(
            f"   📎 Evidence: {evidence_refs}"
        )

    # Strategic Implications
    print("\n💡 STRATEGIC IMPLICATIONS")

    for implication in (
        analysis.strategic_implications
    ):
        print(
            f"• {implication}"
        )

    # Risks and Limitations
    print("\n⚠️ RISKS & LIMITATIONS")

    for risk in (
        analysis.risks_and_limitations
    ):
        print(
            f"• {risk}"
        )

    # What to Watch Next
    print("\n👀 WHAT TO WATCH NEXT")

    for signal in (
        analysis.what_to_watch_next
    ):
        print(
            f"• {signal}"
        )

    # Confidence
    print("\n🎯 CONFIDENCE")
    print(
        f"Level: {analysis.confidence.level}"
    )
    print(
        f"Reason: {analysis.confidence.reason}"
    )

    # ------------------------------------------------
    # 8. Save Markdown report
    # ------------------------------------------------

    report_path = save_report(
        topic,
        analysis,
        sources,
        evidence,
    )

    print(
        f"\n💾 Report saved to: {report_path}"
    )


if __name__ == "__main__":
    main()