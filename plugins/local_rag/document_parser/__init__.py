from typing import Callable, Type

from ..document import Document, DocumentPart, DocumentType, ImagePart, TextPart
from ..utils import Registry, import_submodules
from .config import DocumentParserConfig
from .document_parser import DocumentParser

__all__ = [
    "AutoDocumentParser",
    "Document",
    "DocumentPart",
    "DocumentParser",
    "DocumentParserConfig",
    "DocumentType",
    "ImagePart",
    "TextPart",
]


class AutoDocumentParser(Registry):
    _registry: dict[DocumentType, Callable[[], DocumentParser]] = {}

    @classmethod
    def key_type(cls) -> Type[DocumentType]:
        return DocumentType

    @classmethod
    def base_class(cls) -> Type[DocumentParser]:
        return DocumentParser

    @classmethod
    def get_class(cls, key: DocumentType, default=None) -> Type[DocumentParser]:
        get_func = cls._registry.get(key)
        return get_func() if get_func is not None else default

    @classmethod
    def from_config(cls, class_config: DocumentParserConfig) -> DocumentParser | None:
        class_type = cls.get_class(class_config.doc_type)
        if class_type is None:
            raise ValueError(
                f"DocumentParser type '{class_config.doc_type}' not found.\n"
                f"Available types:\n{cls.get_all_keys()}"
            )
        else:
            return class_type(class_config)


import_submodules(submodule_path=__file__)
