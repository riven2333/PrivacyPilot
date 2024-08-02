from pathlib import Path

from .document import DocumentType

__all__ = ["FileCollector"]


class FileCollector:
    def __init__(
        self, directory: str | Path, extension_to_type: dict[str, DocumentType]
    ) -> None:
        self.directory: Path = (
            Path(directory) if isinstance(directory, str) else directory
        )
        self.extension_to_type: dict[str, DocumentType] = extension_to_type

    def collect_files(self) -> dict[DocumentType, list[Path]]:
        file_dict: dict[DocumentType, list[Path]] = {
            document_type: [] for document_type in DocumentType
        }
        for file_path in self.directory.rglob("*"):
            if not file_path.is_file():
                continue
            extension = file_path.suffix.lower()
            if extension in self.extension_to_type:
                file_dict[self.extension_to_type[extension]].append(file_path)
        return file_dict
