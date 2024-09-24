from typing import Type

from .. import AutoDocumentParser, DocumentParser, DocumentType

__all__ = ["get_text_document_parser_class"]


@AutoDocumentParser.register(DocumentType.text)
def get_text_document_parser_class() -> Type[DocumentParser]:
    from .text_document_parser import TextDocumentParser

    return TextDocumentParser
