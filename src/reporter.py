from datetime import datetime
from pathlib import Path


def save_report(topic, analysis, sources):
    """Save structured intelligence analysis as a Markdown report."""

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    safe_topic = topic.lower().replace(" ", "-")
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")

    filename = reports_dir / f"{safe_topic}_{date}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write("# Strategic Intelligence Brief\n\n")

        file.write(f"**Topic:** {topic}\n\n")
        file.write(f"**Sources analyzed:** {min(len(sources), 5)}\n\n")
        file.write("---\n\n")

        # Raw facts
        file.write("## Raw Facts\n\n")

        for fact in analysis.raw_facts:
            file.write(f"- {fact}\n")

        # Strategic interpretation
        file.write("\n## Strategic Interpretation\n\n")

        for insight in analysis.strategic_interpretation:
            file.write(f"- {insight}\n")

        # Confidence
        file.write("\n## Confidence\n\n")
        file.write(f"**Level:** {analysis.confidence.level}\n\n")
        file.write(f"**Reason:** {analysis.confidence.reason}\n")

        # Sources
        file.write("\n---\n\n")
        file.write("## Sources\n\n")

        for source in sources[:5]:
            file.write(
                f"- [{source['title']}]({source['url']})\n"
            )

    return filename