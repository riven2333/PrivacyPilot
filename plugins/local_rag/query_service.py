from .document.document import DocumentPart
from .embedder import Embedder
from .reranker import Reranker
from .vector_index import VectorIndex

__all__ = ["QueryService"]


class QueryService:
    def __init__(
        self, embedder: Embedder, vector_index: VectorIndex, reranker: Reranker
    ) -> None:
        self.embedder = embedder
        self.vector_index = vector_index
        self.reranker = reranker

    def query(self, query_text: str, k: int = 5) -> list[DocumentPart]:
        try:
            query_embedding = self.embedder.encode_text(query_text)
            doc_parts = self.vector_index.search(query_embedding, query_text, k)
            doc_parts = self.reranker.rerank(query_text, doc_parts)
            return doc_parts
        except Exception as e:
            print(f"Error during query: {e}")
            return []
