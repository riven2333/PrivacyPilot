from pathlib import Path

from .. import Document, DocumentLoader, DocumentLoaderConfig, DocumentType, TextPart

__all__ = ["TextDocumentLoader"]


class TextDocumentLoader(DocumentLoader):
    def __init__(self, config: DocumentLoaderConfig) -> None:
        self._config = config

    def load_document(self, file_path: Path, root_path: Path | None = None) -> Document:
        text = file_path.read_text(encoding="utf-8")
        metadata = {
            "file_path": str(file_path)
            if root_path is None
            else str(file_path.relative_to(root_path))
        }
        return Document([TextPart(text)], metadata)

    @property
    def file_extensions(self) -> list[str]:
        return [".txt"]

    @property
    def file_type(self) -> DocumentType:
        return DocumentType.text
