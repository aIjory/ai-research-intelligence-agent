import faiss
import numpy as np

from semantic_ranker import model


class VectorStore:
    """FAISS vector store for article chunks."""

    def __init__(self):
        self.index = None
        self.chunks = []

    def add_chunks(self, chunks):
        """Create embeddings and store chunks in FAISS."""

        if not chunks:
            return

        embeddings = model.encode(
            chunks,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

        self.chunks = chunks

    def search(self, query, top_k=5):
        """Retrieve chunks most relevant to a query."""

        if self.index is None or not self.chunks:
            return []

        query_embedding = model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks)),
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append(
                {
                    "text": self.chunks[index],
                    "score": float(score),
                }
            )

        return results