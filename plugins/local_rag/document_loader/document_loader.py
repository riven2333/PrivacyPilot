from abc import ABC, abstractmethod
from pathlib import Path

from ..document import Document, DocumentType

__all__ = ["DocumentLoader"]


class DocumentLoader(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def load_document(self, file_path: Path, root_path: Path | None = None) -> Document:
        pass

    @property
    def file_extensions(self) -> list[str]:
        raise NotImplementedError("file_extensions must be implemented")

    @property
    def file_type(self) -> DocumentType:
        raise NotImplementedError("file_type must be implemented")
