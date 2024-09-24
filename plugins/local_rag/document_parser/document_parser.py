from abc import ABC, abstractmethod

from ..document import Document

__all__ = ["DocumentParser"]


class DocumentParser(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def parse(self, document: Document) -> Document:
        pass
