from .. import DocumentPart, Reranker, RerankerConfig

__all__ = ["IdentityReranker"]


class IdentityReranker(Reranker):
    def __init__(self, config: RerankerConfig) -> None:
        self._config = config

    def compute_scores(
        self, query: str, document_parts: list[DocumentPart]
    ) -> list[float]:
        score = 1 / max(1, len(document_parts))
        return [score for _ in document_parts]

    def rerank(
        self, query: str, document_parts: list[DocumentPart]
    ) -> list[DocumentPart]:
        return document_parts
