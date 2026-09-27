import json

from analyzer import client
from models import IntelligenceAnalysis


def analyze_rag_evidence(topic, evidence):
    """
    Analyze retrieved RAG evidence using the LLM.

    The model must ground its analysis exclusively in the
    retrieved evidence and reference supporting evidence IDs.
    """

    if not evidence:
        raise ValueError(
            "No RAG evidence was provided."
        )

    evidence_text = ""

    for index, item in enumerate(
        evidence,
        start=1,
    ):
        evidence_text += f"""
Evidence {index}
Source: {item['source']}
Title: {item['title']}
URL: {item['url']}
Similarity Score: {item['score']:.3f}

Content:
{item['text']}

---
"""

    prompt = f"""
You are a strategic technology research analyst.

Research topic:
{topic}

Analyze ONLY the retrieved evidence provided below.

Your job is to produce a concise strategic intelligence
brief grounded entirely in the supplied evidence.

Return ONLY valid JSON using exactly this structure:

{{
    "executive_summary": "A concise summary of the most important findings.",

    "key_developments": [
        {{
            "title": "Short development title",
            "finding": "Evidence-grounded explanation of the development.",
            "evidence_ids": [1, 3]
        }}
    ],

    "strategic_implications": [
        "Strategic implication 1",
        "Strategic implication 2"
    ],

    "risks_and_limitations": [
        "Risk or limitation 1",
        "Risk or limitation 2"
    ],

    "what_to_watch_next": [
        "Future signal or development to monitor",
        "Another future signal"
    ],

    "confidence": {{
        "level": "High",
        "reason": "Explanation of confidence based on evidence quality and coverage."
    }}
}}

STRICT RULES:

1. Use ONLY the supplied evidence.
2. Do not invent facts, companies, products, events, or capabilities.
3. Every key development must contain one or more valid evidence_ids.
4. evidence_ids must refer only to evidence numbers supplied below.
5. Do not cite evidence that does not directly support the finding.
6. Separate factual findings from strategic interpretation.
7. Strategic implications must logically follow from the evidence.
8. Risks and limitations should identify gaps, uncertainty,
   weak coverage, conflicting evidence, or practical limitations
   supported by the evidence.
9. "What to watch next" should describe signals worth monitoring,
   not invented future events.
10. If the evidence does not strongly support the research topic,
    explicitly state that limitation.
11. Confidence must be High, Medium, or Low.
12. Do not include markdown.
13. Do not include text before or after the JSON.
14. Keep the response concise and avoid repeating the same point.

Retrieved evidence:

{evidence_text}
"""

    response = client.chat.completions.create(
        model="Qwen/Qwen3-4B-Instruct-2507",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=1400,
    )

    raw_response = (
        response
        .choices[0]
        .message
        .content
    )

    try:
        data = json.loads(raw_response)

        analysis = (
            IntelligenceAnalysis.model_validate(
                data
            )
        )

    except (
        json.JSONDecodeError,
        ValueError,
    ) as error:
        raise ValueError(
            "LLM returned an invalid RAG "
            f"response: {error}"
        )

    # Validate evidence references ourselves.
    max_evidence_id = len(evidence)

    for development in (
        analysis.key_developments
    ):
        if not development.evidence_ids:
            raise ValueError(
                "A key development was returned "
                "without evidence IDs."
            )

        for evidence_id in (
            development.evidence_ids
        ):
            if (
                evidence_id < 1
                or evidence_id > max_evidence_id
            ):
                raise ValueError(
                    "LLM referenced invalid "
                    f"evidence ID: {evidence_id}"
                )

    return analysis