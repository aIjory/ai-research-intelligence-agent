"""
Central configuration for the AI Research Intelligence Agent.

Keeping pipeline parameters here makes experiments reproducible
and prevents retrieval settings from being scattered across modules.
"""

# ============================================================
# Research collection
# ============================================================

ARTICLE_LOOKBACK_DAYS = 365

COLLECTOR_CANDIDATE_LIMIT = 100
SEMANTIC_TOP_K = 50
SEMANTIC_SCORE_THRESHOLD = 0.35

DEFAULT_MAX_ARTICLES = 15


# ============================================================
# RAG knowledge base
# ============================================================

RAG_MAX_ARTICLES = 5

# Final number of evidence chunks supplied to the analyzer
RAG_TOP_K = 8

# Retrieve a broader pool before cross-encoder reranking
RAG_CANDIDATE_MULTIPLIER = 4
RAG_MIN_CANDIDATES = 20

VECTOR_MIN_SCORE = 0.25

# Prevent a single article from dominating the context
MAX_CHUNKS_PER_SOURCE = 2


# ============================================================
# Models
# ============================================================

CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L6-v2"


# ============================================================
# Evaluation
# ============================================================

EVALUATION_K = 5