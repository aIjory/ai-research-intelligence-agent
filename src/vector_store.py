import faiss
import numpy as np

from semantic_ranker import model


class VectorStore:
    """
    FAISS vector store that keeps chunk text
    and metadata together.
    """

    def __init__(self):
        self.index = None
        self.documents = []

    def add_documents(self, documents):
        """
        Add documents to the vector store.

        Each document must contain:
        {
            "text": "...",
            "title": "...",
            "url": "...",
            "source": "..."
        }
        """

        if not documents:
            return

        texts = [
            document["text"]
            for document in documents
        ]

        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(
            dimension
        )

        self.index.add(embeddings)

        self.documents = documents

    def search(
        self,
        query,
        top_k=20,
        min_score=0.25,
    ):
        """
        Retrieve candidate chunks from FAISS.

        A relatively permissive threshold is used here
        because a more precise cross-encoder reranker
        will filter the candidates later.
        """

        if (
            self.index is None
            or not self.documents
        ):
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

        search_count = min(
            top_k,
            len(self.documents),
        )

        scores, indices = self.index.search(
            query_embedding,
            search_count,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index == -1:
                continue

            score = float(score)

            if score < min_score:
                continue

            document = self.documents[index]

            results.append(
                {
                    "text": document["text"],
                    "title": document["title"],
                    "url": document["url"],
                    "source": document["source"],
                    "vector_score": score,
                }
            )

        return results