from enum import IntEnum, unique

__all__ = ["DocumentType"]

_doc_name_to_enum: dict[str, "DocumentType"] = {}
_extension_to_enum: dict[str, "DocumentType"] = {}


@unique
class DocumentType(IntEnum):
    unknown = 0
    text = 1
    pdf = 2
    markdown = 3

    @classmethod
    def init_enums(cls) -> None:
        cls._init_doc_name_to_enum()
        cls._init_extension_to_enum()

    @classmethod
    def _init_doc_name_to_enum(cls) -> None:
        name_to_enum = cls._get_name_to_enum()
        if not name_to_enum:
            native_name_to_enum = {
                cls.unknown.name: cls.unknown,
                cls.text.name: cls.text,
                cls.pdf.name: cls.pdf,
                cls.markdown.name: cls.markdown,
            }
            cls._update_name_to_enum(name_to_enum, native_name_to_enum)
        else:
            raise RuntimeError(f"Cannot re-initialize due to {len(name_to_enum)=}!")

    @classmethod
    def _init_extension_to_enum(cls) -> None:
        extension_to_enum = cls._get_extension_to_enum()
        if not extension_to_enum:
            native_extension_to_enum = {
                ".txt": cls.text,
                ".pdf": cls.pdf,
                ".md": cls.markdown,
            }
            cls._update_name_to_enum(extension_to_enum, native_extension_to_enum)
        else:
            raise RuntimeError(
                f"Cannot re-initialize due to {len(extension_to_enum)=}!"
            )

    @staticmethod
    def from_name_or_extension(name_or_extension: str) -> "DocumentType":
        name_to_enum = DocumentType._get_name_to_enum()
        extension_to_enum = DocumentType._get_extension_to_enum()
        return name_to_enum.get(
            name_or_extension,
            extension_to_enum.get(name_or_extension, DocumentType.unknown),
        )

    @staticmethod
    def from_name(name: str) -> "DocumentType":
        name_to_enum = DocumentType._get_name_to_enum()
        return name_to_enum.get(name, DocumentType.unknown)

    @staticmethod
    def from_extension(extension: str) -> "DocumentType":
        extension_to_enum = DocumentType._get_extension_to_enum()
        return extension_to_enum.get(extension, DocumentType.unknown)

    @staticmethod
    def _get_name_to_enum() -> dict[str, "DocumentType"]:
        global _doc_name_to_enum
        return _doc_name_to_enum

    @staticmethod
    def _get_extension_to_enum() -> dict[str, "DocumentType"]:
        global _extension_to_enum
        return _extension_to_enum

    @staticmethod
    def _update_name_to_enum(
        name_to_enum: dict[str, "DocumentType"], new_items: dict[str, "DocumentType"]
    ) -> None:
        for name, enum in new_items.items():
            if name not in name_to_enum:
                name_to_enum[name] = enum


DocumentType.init_enums()
