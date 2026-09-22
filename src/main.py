from collector import collect_research
from analyzer import analyze_research


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    topic = input("What topic would you like to research? ")

    print(f"\n🔎 Research topic: {topic}")

    sources = collect_research(topic)

    print(f"\n📚 Sources collected: {len(sources)}")

    for source in sources:
        print(f"\n📰 {source['title']}")
        print(f"🔗 {source['url']}")

    print("\n🧠 Analyzing research with AI...")

    analysis = analyze_research(topic, sources)

    print("\n" + "=" * 60)
    print("STRATEGIC INTELLIGENCE BRIEF")
    print("=" * 60)
    print(analysis)


if __name__ == "__main__":
    main()