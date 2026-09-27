from article_extractor import extract_article_text
from chunker import chunk_text
from vector_store import VectorStore


def build_rag_context(topic, articles, max_articles=5, top_k=8):
    """
    Extract article content, chunk it, store it in FAISS,
    and retrieve the most relevant evidence for the topic.
    """

    all_chunks = []
    chunk_metadata = []

    print("\n📚 Building RAG knowledge base...")

    # Use the highest-ranked articles
    for article in articles[:max_articles]:
        print(f"   Extracting: {article['title']}")

        text = extract_article_text(article["url"])

        if not text:
            print("   ⚠️ No article text extracted.")
            continue

        chunks = chunk_text(text)

        print(f"   Created {len(chunks)} chunks.")

        for chunk in chunks:
            all_chunks.append(chunk)

            chunk_metadata.append(
                {
                    "title": article["title"],
                    "url": article["url"],
                    "source": article["source"],
                }
            )

    if not all_chunks:
        print("   ⚠️ No usable article content found.")
        return []

    print(
        f"\n🧩 Total chunks in knowledge base: "
        f"{len(all_chunks)}"
    )

    # Create FAISS vector store
    store = VectorStore()
    store.add_chunks(all_chunks)

    # Retrieve the chunks most relevant to the topic
    retrieved = store.search(
        topic,
        top_k=top_k,
    )

    # Add source metadata back to each retrieved chunk
    for result in retrieved:
        chunk_index = all_chunks.index(result["text"])
        metadata = chunk_metadata[chunk_index]

        result["title"] = metadata["title"]
        result["url"] = metadata["url"]
        result["source"] = metadata["source"]

    return retrieved