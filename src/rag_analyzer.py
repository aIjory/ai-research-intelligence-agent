import json

from analyzer import client
from models import IntelligenceAnalysis


def analyze_rag_evidence(topic, evidence):
    """
    Analyze retrieved RAG evidence using the LLM.
    """

    if not evidence:
        raise ValueError("No RAG evidence was provided.")

    evidence_text = ""

    for index, item in enumerate(evidence, start=1):
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

Return ONLY valid JSON using exactly this structure:

{{
    "raw_facts": [
        "Fact 1",
        "Fact 2"
    ],
    "strategic_interpretation": [
        "Interpretation 1",
        "Interpretation 2"
    ],
    "confidence": {{
        "level": "High",
        "reason": "Explanation"
    }}
}}

Rules:
- Use only the supplied evidence.
- Do not invent facts.
- Separate factual findings from interpretation.
- Do not include markdown.
- Do not include text before or after the JSON.
- Confidence must be High, Medium, or Low.
- If evidence is limited or conflicting, lower the confidence.

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
        max_tokens=900,
    )

    raw_response = response.choices[0].message.content

    try:
        data = json.loads(raw_response)

        return IntelligenceAnalysis.model_validate(data)

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"LLM returned an invalid RAG response: {error}"
        )