import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN was not found in the .env file.")

client = InferenceClient(api_key=HF_TOKEN)


def analyze_research(topic, sources):
    """Analyze collected research using an LLM."""

    if not sources:
        return "No sources were found to analyze."

    research_text = ""

    for source in sources[:5]:
        research_text += f"""
Title: {source['title']}
Summary: {source['summary']}
Source: {source['url']}
"""

    prompt = f"""
You are a strategic technology research analyst.

Research topic:
{topic}

Based ONLY on the research sources provided below, produce a concise
strategic intelligence analysis.

Separate your response into:

1. RAW FACTS
- Extract important factual developments.
- Do not add unsupported information.

2. STRATEGIC INTERPRETATION
- Explain what these developments could mean.
- Clearly distinguish interpretation from fact.

3. CONFIDENCE
- Give a confidence level: High, Medium, or Low.
- Briefly explain why.

Research sources:
{research_text}
"""

    response = client.chat.completions.create(
        model="Qwen/Qwen3-4B-Instruct-2507",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=700,
    )

    return response.choices[0].message.content