from abc import ABC, abstractmethod

from numpy import ndarray

from ..document import Document

__all__ = ["Embedder"]


class Embedder(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def encode_text(self, text: str | list[str]) -> ndarray:
        pass

    @abstractmethod
    def create_embeddings(self, documents: list[Document]) -> list[Document]:
        pass

    @abstractmethod
    def dimension(self) -> int:
        pass
