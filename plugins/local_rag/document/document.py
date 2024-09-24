from abc import ABC, abstractmethod

from numpy import ndarray

__all__ = ["Document", "DocumentPart", "ImagePart", "TextPart"]


class DocumentPart(ABC):
    def __init__(self, metadata: dict | None = None):
        self._embedding: ndarray | None = None
        self._metadata: dict = metadata if metadata is not None else {}

    @property
    def embedding(self) -> ndarray | None:
        return self._embedding

    @embedding.setter
    def embedding(self, value: ndarray) -> None:
        if isinstance(value, ndarray):
            self._embedding = value

    @property
    def metadata(self) -> dict:
        return self._metadata.copy()

    @abstractmethod
    def get_data(self) -> str | bytes:
        pass


class TextPart(DocumentPart):
    def __init__(self, text: str, metadata: dict | None = None) -> None:
        super().__init__(metadata)
        self._text: str = text

    @property
    def text(self) -> str:
        return self._text

    def get_data(self) -> str:
        return self.text


class ImagePart(DocumentPart):
    def __init__(
        self,
        image_data: bytes,
        caption: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        super().__init__(metadata)
        self._image_data: bytes = image_data
        self._caption: str | None = caption

    @property
    def image_data(self) -> bytes:
        return self._image_data

    @property
    def caption(self) -> str | None:
        return self._caption

    def get_data(self) -> bytes:
        return self.image_data


class Document:
    def __init__(self, parts: list[DocumentPart], metadata: dict | None = None) -> None:
        self.parts: list[DocumentPart] = parts
        self.metadata: dict = metadata if metadata is not None else {}
