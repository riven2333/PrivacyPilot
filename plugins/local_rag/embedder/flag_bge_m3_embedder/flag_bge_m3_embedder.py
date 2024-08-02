from numpy import ndarray

from .. import Document, Embedder, EmbedderConfig

__all__ = ["FlagBGEM3Embedder"]


class FlagBGEM3Embedder(Embedder):
    def __init__(self, config: EmbedderConfig) -> None:
        self._config = config
        self._model = self._load_model(config)

    @staticmethod
    def _load_model(config: EmbedderConfig):
        model_name = "BAAI/bge-m3"
        if config.endpoint is not None or config.cache_folder is not None:
            import os

            old_endpoint = os.environ.get("HF_ENDPOINT")
            old_cache_folder = os.environ.get("HF_HUB_CACHE")
            os.environ["HF_ENDPOINT"] = config.endpoint
            os.environ["HF_HUB_CACHE"] = config.cache_folder

            from FlagEmbedding import BGEM3FlagModel

            model = BGEM3FlagModel(model_name)

            if old_endpoint is not None:
                os.environ["HF_ENDPOINT"] = old_endpoint
            else:
                del os.environ["HF_ENDPOINT"]

            if old_cache_folder is not None:
                os.environ["HF_HUB_CACHE"] = old_cache_folder
            else:
                del os.environ["HF_HUB_CACHE"]
        else:
            from FlagEmbedding import BGEM3FlagModel

            model = BGEM3FlagModel(model_name)
        return model

    def encode_text(self, text: str | list[str]) -> ndarray:
        if isinstance(text, str):
            text = [text]
        elif isinstance(text, list):
            pass
        else:
            raise ValueError("text must be a string or a list of strings")
        return self._model.encode(text)["dense_vecs"]

    def create_embeddings(self, documents: list[Document]) -> list[Document]:
        parts = []
        for document in documents:
            parts.extend(document.parts)
        if not parts:
            return documents

        batch_size = 1 if self._config.batch_size is None else self._config.batch_size
        embeddings = self._model.encode(
            [part.get_data() for part in parts], batch_size=batch_size
        )["dense_vecs"]
        for i, part in enumerate(parts):
            part.embedding = embeddings[i]
        return documents

    def dimension(self) -> int:
        return self._model.model.model.config.hidden_size
