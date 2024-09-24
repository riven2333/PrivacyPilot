import json
from functools import cache
from pathlib import Path

from .document_loader.config import DocumentLoaderConfigs
from .document_parser.config import DocumentParserConfigs
from .embedder.config import EmbedderConfig
from .reranker.config import RerankerConfig
from .utils import change_sub_dir
from .vector_index.config import VectorIndexConfig

__all__ = ["Config"]


@cache
class Config:
    def __init__(self, config_path: str | Path) -> None:
        config = self.load_config(config_path)
        with change_sub_dir(Path(config_path).parent):
            self._parse_config(config)

    @staticmethod
    def load_config(config_path: str | Path) -> dict:
        try:
            with open(config_path, "r") as file:
                config = json.load(file) or {}
        except Exception as err:
            print(f"Invalid config file: {err}")
            config = {}
        return config

    def _parse_config(self, config: dict) -> None:
        self.data_directory: Path = Path(
            config.get("data_directory", "./data")
        ).resolve()

        document_loader_configs = config.get("document_loader_configs", [])
        self.document_loader_configs = DocumentLoaderConfigs(document_loader_configs)

        document_parser_configs = config.get("document_parser_configs", [])
        self.document_parser_configs = DocumentParserConfigs(document_parser_configs)

        embedder_config = config.get("embedder_config", {})
        self.embedder_config = EmbedderConfig(embedder_config)

        vector_index_config = config.get("vector_index_config", {})
        self.vector_index_config = VectorIndexConfig(vector_index_config)

        reranker_config = config.get("reranker_config", {})
        self.reranker_config = RerankerConfig(reranker_config)
