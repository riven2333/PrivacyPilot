from functools import cache
from pathlib import Path

from .config import Config
from .document import Document
from .document_loader import AutoDocumentLoader
from .document_parser import AutoDocumentParser
from .document_processor import DocumentProcessor
from .embedder import AutoEmbedder
from .file_collector import FileCollector
from .query_service import QueryService
from .reranker import AutoReranker
from .vector_index import AutoVectorIndex


@cache
class LocalRAG:
    def __init__(self, config_path: str | Path) -> None:
        self._config = Config(config_path)
        self._init_document_collector_and_processor()

        self._embedder = AutoEmbedder.from_config(self._config.embedder_config)

        dimension = self._config.vector_index_config.dimension
        self._config.vector_index_config.dimension = (
            dimension if dimension is not None else self._embedder.dimension()
        )

        self._vector_index = AutoVectorIndex.from_config(
            self._config.vector_index_config
        )

        self._reranker = AutoReranker.from_config(self._config.reranker_config)

        self._query_service = QueryService(
            self._embedder, self._vector_index, self._reranker
        )

        self._documents: list[Document] = []
        self._processed = False

    def _init_document_collector_and_processor(self) -> None:
        doc_type_to_loader_config = {
            config.doc_type: config for config in self._config.document_loader_configs
        }
        doc_type_to_parser_config = {
            config.doc_type: config for config in self._config.document_parser_configs
        }

        valid_doc_types = [
            doc_type
            for doc_type in doc_type_to_loader_config
            if doc_type in doc_type_to_parser_config
            and AutoDocumentLoader.has(doc_type)
            and AutoDocumentParser.has(doc_type)
        ]
        extension_to_type = {
            doc_type_to_loader_config[doc_type].extension: doc_type
            for doc_type in valid_doc_types
        }
        self._file_collector = FileCollector(
            self._config.data_directory, extension_to_type
        )

        loaders = {
            doc_type: AutoDocumentLoader.from_config(
                doc_type_to_loader_config[doc_type]
            )
            for doc_type in valid_doc_types
        }
        parsers = {
            doc_type: AutoDocumentParser.from_config(
                doc_type_to_parser_config[doc_type]
            )
            for doc_type in valid_doc_types
        }
        self._document_processor = DocumentProcessor(
            loaders, parsers, self._config.data_directory
        )

    @property
    def processed(self) -> bool:
        return self._processed

    def process_files(self, force_reprocess: bool = False) -> None:
        if self._processed and not force_reprocess:
            return
        file_dict = self._file_collector.collect_files()
        documents = self._document_processor.process_documents(file_dict)
        self._documents = self._embedder.create_embeddings(documents)
        self._vector_index.clear()
        self._vector_index.add_documents(self._documents)
        self._processed = True

    def query(
        self, query_text: str, k: int = 5, force_reprocess: bool = False
    ) -> list[str | bytes]:
        if force_reprocess:
            self.process_files(force_reprocess)
        doc_parts = self._query_service.query(query_text, k)
        return [doc_part.get_data() for doc_part in doc_parts]
