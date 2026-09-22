from collector import collect_research
from analyzer import analyze_research
from reporter import save_report


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    topic = input("What topic would you like to research? ")

    print(f"\n🔎 Research topic: {topic}")

    # Collect research sources
    sources = collect_research(topic)

    print(f"\n📚 Sources collected: {len(sources)}")

    for source in sources:
        print(f"\n📰 {source['title']}")
        print(f"🔗 {source['url']}")

    # Analyze research
    print("\n🧠 Analyzing research with AI...")

    analysis = analyze_research(topic, sources)

    # Display structured analysis
    print("\n" + "=" * 60)
    print("STRATEGIC INTELLIGENCE BRIEF")
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

    # Save report
    report_path = save_report(topic, analysis, sources)

    print(f"\n💾 Report saved to: {report_path}")


if __name__ == "__main__":
    main()