from ..document import DocumentType

__all__ = ["DocumentLoaderConfig", "DocumentLoaderConfigs"]


class DocumentLoaderConfigs:
    def __init__(self, document_loader_configs: list[dict]) -> None:
        self._configs = [
            DocumentLoaderConfig(config) for config in document_loader_configs
        ]

    def __iter__(self):
        return iter(self._configs)

    def __getitem__(self, index: int) -> "DocumentLoaderConfig":
        return self._configs[index]

    def __len__(self) -> int:
        return len(self._configs)


class DocumentLoaderConfig:
    def __init__(self, document_loader_config: dict) -> None:
        self.extension: str = document_loader_config.get("extension", "")

    @property
    def doc_type(self) -> DocumentType:
        return DocumentType.from_extension(self.extension)
