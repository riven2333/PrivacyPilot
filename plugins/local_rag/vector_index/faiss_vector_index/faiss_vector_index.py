import faiss
from numpy import asarray, ndarray

from .. import Document, DocumentPart, VectorIndex, VectorIndexConfig

__all__ = ["FaissVectorIndex"]


class FaissVectorIndex(VectorIndex):
    def __init__(self, config: VectorIndexConfig) -> None:
        self._index = faiss.IndexFlatL2(config.dimension)
        self._document_parts: list[DocumentPart] = []

    def add_documents(self, documents: list[Document]) -> None:
        for document in documents:
            for part in document.parts:
                self._document_parts.append(part)

        embeddings = [part.embedding for part in self._document_parts]
        if embeddings:
            self._index.add(asarray(embeddings))

    def search(
        self, query_embedding: ndarray, query: str | None = None, k: int = 5
    ) -> list[DocumentPart]:
        distances, indices = self._index.search(query_embedding, k)
        return [self._document_parts[i] for i in indices[0]]

    def clear(self) -> None:
        self._index.reset()
        self._document_parts = []
