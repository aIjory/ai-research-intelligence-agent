from datetime import datetime
from pathlib import Path


def save_report(
    topic,
    analysis,
    sources,
    evidence=None,
):
    """
    Save a source-traceable strategic intelligence
    brief as Markdown.
    """

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    safe_topic = (
        topic.lower()
        .replace(" ", "-")
    )

    date = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    filename = (
        reports_dir
        / f"{safe_topic}_{date}.md"
    )

    evidence = evidence or []

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        # ====================================================
        # Header
        # ====================================================

        file.write(
            "# Strategic Intelligence Brief\n\n"
        )

        file.write(
            f"**Topic:** {topic}\n\n"
        )

        file.write(
            f"**Generated:** "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        )

        file.write(
            f"**Sources collected:** "
            f"{len(sources)}\n\n"
        )

        file.write(
            f"**Evidence chunks analyzed:** "
            f"{len(evidence)}\n\n"
        )

        file.write("---\n\n")

        # ====================================================
        # Executive summary
        # ====================================================

        file.write(
            "## Executive Summary\n\n"
        )

        file.write(
            f"{analysis.executive_summary}\n\n"
        )

        # ====================================================
        # Key developments
        # ====================================================

        file.write(
            "## Key Developments\n\n"
        )

        for index, development in enumerate(
            analysis.key_developments,
            start=1,
        ):
            file.write(
                f"### {index}. "
                f"{development.title}\n\n"
            )

            file.write(
                f"{development.finding}\n\n"
            )

            references = ", ".join(
                f"E{evidence_id}"
                for evidence_id
                in development.evidence_ids
            )

            file.write(
                f"**Evidence:** "
                f"{references}\n\n"
            )

        # ====================================================
        # Strategic implications
        # ====================================================

        file.write(
            "## Strategic Implications\n\n"
        )

        for implication in (
            analysis.strategic_implications
        ):
            file.write(
                f"- {implication}\n"
            )

        # ====================================================
        # Risks and limitations
        # ====================================================

        file.write(
            "\n## Risks & Limitations\n\n"
        )

        for risk in (
            analysis.risks_and_limitations
        ):
            file.write(
                f"- {risk}\n"
            )

        # ====================================================
        # What to watch next
        # ====================================================

        file.write(
            "\n## What to Watch Next\n\n"
        )

        for signal in (
            analysis.what_to_watch_next
        ):
            file.write(
                f"- {signal}\n"
            )

        # ====================================================
        # Confidence
        # ====================================================

        file.write(
            "\n## Confidence\n\n"
        )

        file.write(
            f"**Level:** "
            f"{analysis.confidence.level}\n\n"
        )

        file.write(
            f"**Reason:** "
            f"{analysis.confidence.reason}\n"
        )

        # ====================================================
        # Evidence register
        # ====================================================

        if evidence:
            file.write(
                "\n---\n\n"
            )

            file.write(
                "## Evidence Register\n\n"
            )

            for index, item in enumerate(
                evidence,
                start=1,
            ):
                file.write(
                    f"### E{index} — "
                    f"{item['title']}\n\n"
                )

                file.write(
                    f"**Source:** "
                    f"{item['source']}\n\n"
                )

                file.write(
                    f"**URL:** "
                    f"{item['url']}\n\n"
                )

                if "score" in item:
                    file.write(
                        f"**Vector similarity:** "
                        f"{item['score']:.3f}\n\n"
                    )

        # ====================================================
        # Sources
        # ====================================================

        file.write(
            "\n---\n\n"
        )

        file.write(
            "## Sources\n\n"
        )

        seen_urls = set()

        for source in sources:

            url = source["url"]

            if url in seen_urls:
                continue

            seen_urls.add(url)

            file.write(
                f"- [{source['title']}]"
                f"({url}) — "
                f"{source['source']}\n"
            )

    return filename