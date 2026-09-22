import json
import os
from pathlib import Path

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from models import IntelligenceAnalysis


# Load environment variables
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN was not found in the .env file.")


# Initialize Hugging Face client
client = InferenceClient(api_key=HF_TOKEN)


def analyze_research(topic, sources):
    """Analyze collected research using an LLM."""

    if not sources:
        raise ValueError("No research sources were found to analyze.")

    # Use the first five sources
    research_text = ""

    for source in sources[:5]:
        research_text += f"""
Title: {source['title']}
Summary: {source['summary']}
Source: {source['url']}

"""

    # Ask the model for structured JSON
    prompt = f"""
You are a strategic technology research analyst.

Research topic:
{topic}

Analyze ONLY the research sources provided below.

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
- Do not include markdown.
- Do not include text before or after the JSON.
- raw_facts must contain only information supported by the sources.
- strategic_interpretation must clearly be interpretation, not fact.
- confidence level must be High, Medium, or Low.

Research sources:

{research_text}
"""

    # Send request to Hugging Face
    response = client.chat.completions.create(
        model="Qwen/Qwen3-4B-Instruct-2507",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=700,
    )

    # Extract model response
    raw_response = response.choices[0].message.content

    # Convert JSON response into validated Pydantic model
    try:
        data = json.loads(raw_response)
        analysis = IntelligenceAnalysis.model_validate(data)

        return analysis

    except (json.JSONDecodeError, ValueError) as error:
        raise ValueError(
            f"LLM returned an invalid structured response: {error}"
        )