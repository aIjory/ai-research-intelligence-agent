from collector import collect_research


def main():
    print("\n🤖 AI Research Intelligence Agent")
    print("--------------------------------")

    topic = input("What topic would you like to research? ")

    print(f"\n🔎 Research topic: {topic}")

    # Collect research sources
    sources = collect_research(topic)

    # Display number of sources
    print(f"\n📚 Sources collected: {len(sources)}")

    # Display collected articles
    for source in sources:
        print(f"\n📰 {source['title']}")
        print(f"🔗 {source['url']}")


if __name__ == "__main__":
    main()