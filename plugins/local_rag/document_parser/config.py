from ..document import DocumentType

__all__ = ["DocumentParserConfig", "DocumentParserConfigs"]


class DocumentParserConfigs:
    def __init__(self, document_parser_configs: list[dict]) -> None:
        self._configs = [
            DocumentParserConfig(config) for config in document_parser_configs
        ]

    def __iter__(self):
        return iter(self._configs)

    def __getitem__(self, index: int) -> "DocumentParserConfig":
        return self._configs[index]

    def __len__(self) -> int:
        return len(self._configs)


class DocumentParserConfig:
    def __init__(self, document_parser_config: dict) -> None:
        self.extension: str = document_parser_config.get("extension", "")
        self.char_chunk_size: int = document_parser_config.get("char_chunk_size", 512)
        self.char_overlap_size: int | None = document_parser_config.get(
            "char_overlap_size"
        )

    @property
    def doc_type(self) -> DocumentType:
        return DocumentType.from_extension(self.extension)
