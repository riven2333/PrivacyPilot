from numpy import ndarray, ones

from .. import Document, Embedder, EmbedderConfig

__all__ = ["TestEmbedder"]


class TestEmbedder(Embedder):
    def __init__(self, config: EmbedderConfig) -> None:
        self._config = config

    def encode_text(self, text: str | list[str]) -> ndarray:
        if isinstance(text, list):
            return ones((len(text), 1))
        else:
            return ones((1, 1))

    def create_embeddings(self, documents: list[Document]) -> list[Document]:
        for document in documents:
            for part in document.parts:
                part.embedding = ones(1)
        return documents

    def dimension(self) -> int:
        return 1
