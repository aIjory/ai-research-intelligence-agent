from typing import Literal

from pydantic import BaseModel


class Confidence(BaseModel):
    level: Literal["High", "Medium", "Low"]
    reason: str


class KeyDevelopment(BaseModel):
    title: str
    finding: str
    evidence_ids: list[int]


class IntelligenceAnalysis(BaseModel):
    executive_summary: str

    key_developments: list[KeyDevelopment]

    strategic_implications: list[str]

    risks_and_limitations: list[str]

    what_to_watch_next: list[str]

    confidence: Confidence