from datetime import datetime
from pathlib import Path


def save_report(topic, analysis, sources):
    """Save the intelligence analysis as a Markdown report."""

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

        file.write(analysis)

        file.write("\n\n---\n\n")
        file.write("## Sources\n\n")

        for source in sources[:5]:
            file.write(
                f"- [{source['title']}]({source['url']})\n"
            )

    return filename