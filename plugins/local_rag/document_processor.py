from collections import defaultdict
from concurrent.futures import Future, ThreadPoolExecutor
from multiprocessing import cpu_count
from pathlib import Path

from .document import Document, DocumentType
from .document_loader.document_loader import DocumentLoader
from .document_parser.document_parser import DocumentParser

__all__ = ["DocumentProcessor"]


class DocumentProcessor:
    def __init__(
        self,
        loaders: dict[DocumentType, DocumentLoader],
        parsers: dict[DocumentType, DocumentParser],
        root_path: Path | None = None,
    ) -> None:
        self.loaders = loaders
        self.parsers = parsers
        self.root_path = root_path

    def process_documents(
        self, file_dict: dict[DocumentType, list[Path]]
    ) -> list[Document]:
        n_core = cpu_count() * 2 // 3

        documents = self.load_documents(file_dict, n_core)
        parsed_documents = self.parse_documents(documents, n_core)

        return parsed_documents

    def load_documents(
        self, file_dict: dict[DocumentType, list[Path]], n_core: int
    ) -> dict[DocumentType, list[Document]]:
        documents: dict[DocumentType, list[Document]] = {}
        valid_doc_types = [
            doc_type for doc_type in self.loaders if doc_type in self.parsers
        ]
        type_and_path_pairs = [
            (doc_type, file_path)
            for doc_type in valid_doc_types
            for file_path in file_dict.get(doc_type, [])
        ]
        root_path = self.root_path

        if len(type_and_path_pairs) > 1:
            with ThreadPoolExecutor(
                max_workers=min(n_core, len(type_and_path_pairs))
            ) as executor:
                futures: dict[DocumentType, list[Future[Document]]] = defaultdict(list)
                for doc_type, file_path in type_and_path_pairs:
                    loader = self.loaders[doc_type]
                    futures[doc_type].append(
                        executor.submit(loader.load_document, file_path, root_path)
                    )
                for doc_type, future_list in futures.items():
                    documents[doc_type] = [future.result() for future in future_list]
        else:
            for doc_type, file_path in type_and_path_pairs:
                loader = self.loaders[doc_type]
                if doc_type in documents:
                    documents[doc_type].append(
                        loader.load_document(file_path, root_path)
                    )
                else:
                    documents[doc_type] = [loader.load_document(file_path, root_path)]

        return documents

    def parse_documents(
        self, documents: dict[DocumentType, list[Document]], n_core: int
    ) -> list[Document]:
        type_and_doc_pairs = [
            (doc_type, doc)
            for doc_type, doc_list in documents.items()
            for doc in doc_list
        ]

        if len(type_and_doc_pairs) > 1:
            with ThreadPoolExecutor(
                max_workers=min(n_core, len(type_and_doc_pairs))
            ) as executor:
                futures = [
                    executor.submit(self.parsers[doc_type].parse, doc)
                    for doc_type, doc in type_and_doc_pairs
                ]
                parsed_documents = [future.result() for future in futures]
        else:
            parsed_documents = [
                self.parsers[doc_type].parse(doc)
                for doc_type, doc in type_and_doc_pairs
            ]

        return parsed_documents
