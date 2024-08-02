from typing import Type

from .. import AutoDocumentLoader, DocumentLoader, DocumentType

__all__ = ["get_text_document_loader_class"]


@AutoDocumentLoader.register(DocumentType.text)
def get_text_document_loader_class() -> Type[DocumentLoader]:
    from .text_document_loader import TextDocumentLoader

    return TextDocumentLoader
