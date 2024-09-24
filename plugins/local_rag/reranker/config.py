from pathlib import Path

__all__ = ["RerankerConfig"]


class RerankerConfig:
    def __init__(self, reranker_config: dict):
        self.type: str = reranker_config.get("type", "identity")
        self.model_name: str | None = reranker_config.get("model_name")
        cache_folder: str | None = reranker_config.get("cache_folder")
        cache_folder = (
            str(Path(cache_folder).resolve()) if cache_folder is not None else None
        )
        self.cache_folder: str | None = cache_folder
        self.batch_size: int | None = reranker_config.get("batch_size")
        self.max_seq_length: int | None = reranker_config.get("max_seq_length")
        self.endpoint: str | None = reranker_config.get("endpoint")
