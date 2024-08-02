from abc import ABC, abstractmethod

from ..document import DocumentPart

__all__ = ["Reranker"]


class Reranker(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def compute_scores(
        self, query: str, document_parts: list[DocumentPart]
    ) -> list[float]:
        pass

    @abstractmethod
    def rerank(
        self, query: str, document_parts: list[DocumentPart]
    ) -> list[DocumentPart]:
        pass
