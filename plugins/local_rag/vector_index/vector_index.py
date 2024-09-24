from abc import ABC, abstractmethod

from numpy import ndarray

from ..document import Document, DocumentPart

__all__ = ["VectorIndex"]


class VectorIndex(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> None:
        pass

    @abstractmethod
    def search(
        self, query_embedding: ndarray, query: str | None = None, k: int = 5
    ) -> list[DocumentPart]:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
