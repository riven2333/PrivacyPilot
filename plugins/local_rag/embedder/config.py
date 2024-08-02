from pathlib import Path

__all__ = ["EmbedderConfig"]


class EmbedderConfig:
    def __init__(self, embedder_config: dict) -> None:
        self.type: str = embedder_config.get("type", "flag_bge_m3")
        cache_folder: str | None = embedder_config.get("cache_folder")
        cache_folder = (
            str(Path(cache_folder).resolve()) if cache_folder is not None else None
        )
        self.cache_folder: str | None = cache_folder
        self.batch_size: int | None = embedder_config.get("batch_size")
        self.max_seq_length: int | None = embedder_config.get("max_seq_length")
        self.endpoint: str | None = embedder_config.get("endpoint")
