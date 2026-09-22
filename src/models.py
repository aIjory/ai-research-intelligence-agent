from typing import Literal
from pydantic import BaseModel


class Confidence(BaseModel):
    level: Literal["High", "Medium", "Low"]
    reason: str


class IntelligenceAnalysis(BaseModel):
    raw_facts: list[str]
    strategic_interpretation: list[str]
    confidence: Confidence