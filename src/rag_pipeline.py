from sentence_transformers import CrossEncoder

from article_extractor import extract_article_text
from chunker import chunk_text
from vector_store import VectorStore


chunk_reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


def rerank_chunks(query, candidates):
    """
    Rerank retrieved chunks using a cross-encoder.
    """

    if not candidates:
        return []

    pairs = []

    for candidate in candidates:
        pairs.append(
            [
                query,
                candidate["text"],
            ]
        )

    scores = chunk_reranker.predict(
        pairs
    )

    reranked = []

    for candidate, score in zip(
        candidates,
        scores,
    ):
        result = candidate.copy()

        result["reranker_score"] = float(
            score
        )

        reranked.append(result)

    reranked.sort(
        key=lambda item: item["reranker_score"],
        reverse=True,
    )

    return reranked


def apply_source_diversity(
    results,
    top_k=8,
    max_per_source=2,
):
    """
    Prevent one article from dominating
    the retrieved evidence.
    """

    selected = []
    source_counts = {}

    for result in results:

        source_key = result["url"]

        current_count = source_counts.get(
            source_key,
            0,
        )

        if current_count >= max_per_source:
            continue

        selected.append(result)

        source_counts[source_key] = (
            current_count + 1
        )

        if len(selected) >= top_k:
            break

    return selected


def build_rag_context(
    topic,
    articles,
    max_articles=5,
    top_k=8,
):
    """
    Build a multi-document RAG knowledge base.

    Pipeline:
    1. Extract full article text
    2. Split articles into chunks
    3. Store chunks and metadata in FAISS
    4. Retrieve candidate chunks
    5. Cross-encoder rerank chunks
    6. Apply source diversity
    """

    documents = []

    print(
        "\n📚 Building RAG knowledge base..."
    )

    # --------------------------------------------
    # 1. Extract and chunk articles
    # --------------------------------------------

    for article in articles[:max_articles]:

        print(
            f"   Extracting: "
            f"{article['title']}"
        )

        text = extract_article_text(
            article["url"]
        )

        if not text:
            print(
                "   ⚠️ No article text extracted."
            )
            continue

        chunks = chunk_text(text)

        print(
            f"   Created {len(chunks)} chunks."
        )

        for chunk in chunks:

            documents.append(
                {
                    "text": chunk,
                    "title": article["title"],
                    "url": article["url"],
                    "source": article["source"],
                }
            )

    if not documents:
        print(
            "   ⚠️ No usable article content found."
        )
        return []

    print(
        f"\n🧩 Total chunks in knowledge base: "
        f"{len(documents)}"
    )

    # --------------------------------------------
    # 2. Build FAISS index
    # --------------------------------------------

    store = VectorStore()

    store.add_documents(
        documents
    )

    # --------------------------------------------
    # 3. Broad vector retrieval
    # --------------------------------------------

    candidate_count = min(
        max(top_k * 4, 20),
        len(documents),
    )

    candidates = store.search(
        topic,
        top_k=candidate_count,
        min_score=0.25,
    )

    print(
        f"🔎 FAISS retrieved "
        f"{len(candidates)} candidate chunks."
    )

    if not candidates:
        print(
            "   ⚠️ No chunks passed vector retrieval."
        )
        return []

    # --------------------------------------------
    # 4. Cross-encoder chunk reranking
    # --------------------------------------------

    print(
        f"🧠 Reranking "
        f"{len(candidates)} evidence chunks..."
    )

    reranked = rerank_chunks(
        topic,
        candidates,
    )

    # --------------------------------------------
    # 5. Source diversity
    # --------------------------------------------

    selected = apply_source_diversity(
        reranked,
        top_k=top_k,
        max_per_source=2,
    )

    # Keep compatibility with rag_analyzer.py,
    # which expects result["score"].
    for result in selected:
        result["score"] = result[
            "vector_score"
        ]

    print(
        f"🎯 Selected {len(selected)} "
        f"diverse evidence chunks."
    )

    return selected