from collector import collect_research
from rag_pipeline import build_rag_context
from rag_analyzer import analyze_rag_evidence
from reporter import save_report


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    topic = input("What topic would you like to research? ")

    print(f"\n🔎 Research topic: {topic}")

    # 1. Find and rank relevant articles
    sources = collect_research(topic)

    print(f"\n📚 Sources collected: {len(sources)}")

    if not sources:
        print("\n⚠️ No relevant sources were found.")
        return

    # Display selected articles
    for source in sources:
        print(f"\n📰 {source['title']}")
        print(f"🏢 Source: {source['source']}")
        print(f"📅 Published: {source['published']}")
        print(f"🔗 {source['url']}")

    # 2. Build RAG knowledge base and retrieve evidence
    evidence = build_rag_context(
        topic,
        sources,
        max_articles=5,
        top_k=8,
    )

    if not evidence:
        print("\n⚠️ No usable evidence could be retrieved.")
        return

    print(f"\n🔍 Retrieved {len(evidence)} evidence chunks.")

    # 3. Analyze retrieved evidence with the LLM
    print("\n🧠 Analyzing retrieved evidence with AI...")

    analysis = analyze_rag_evidence(
        topic,
        evidence,
    )

    # 4. Display structured analysis
    print("\n" + "=" * 60)
    print("RAG-GROUNDED STRATEGIC INTELLIGENCE BRIEF")
    print("=" * 60)

    print("\n📌 RAW FACTS")

    for fact in analysis.raw_facts:
        print(f"• {fact}")

    print("\n💡 STRATEGIC INTERPRETATION")

    for insight in analysis.strategic_interpretation:
        print(f"• {insight}")

    print("\n🎯 CONFIDENCE")
    print(f"Level: {analysis.confidence.level}")
    print(f"Reason: {analysis.confidence.reason}")

    # 5. Save report
    report_path = save_report(
        topic,
        analysis,
        sources,
    )

    print(f"\n💾 Report saved to: {report_path}")


if __name__ == "__main__":
    main()