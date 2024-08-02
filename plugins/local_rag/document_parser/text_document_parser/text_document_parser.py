from nltk.tokenize import sent_tokenize

from .. import Document, DocumentParser, DocumentParserConfig, DocumentType, TextPart

__all__ = ["TextDocumentParser"]


class TextDocumentParser(DocumentParser):
    def __init__(self, config: DocumentParserConfig) -> None:
        self._config = config
        self._char_chunk_size = config.char_chunk_size
        self._char_overlap_size = config.char_overlap_size
        self._check_tokenizer()

    @staticmethod
    def _check_tokenizer():
        try:
            sent_tokenize("This is a test sentence.")
        except LookupError:
            import nltk

            nltk.download("punkt")

    def parse(self, document: Document) -> Document:
        sentences = self._split_sentences(document.parts[0].get_data())
        chunks = self._chunk_sentences(sentences)
        document.parts = [TextPart(chunk) for chunk in chunks]
        return document

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        return sent_tokenize(text)

    def _chunk_sentences(self, sentences: list[str]) -> list[str]:
        def locate_overlap_start_index(idx_left: int, idx_right: int):
            overlap_len = 0
            j = idx_right - 1
            while j >= idx_left:
                if overlap_len + len(sentences[j]) > char_overlap_size:
                    break
                overlap_len += len(sentences[j])
                j -= 1
            idx_overlap = j + 1
            return overlap_len, idx_overlap

        char_chunk_size = self._char_chunk_size
        char_overlap_size = self._char_overlap_size
        chunks = []
        cur_chunk_len = len(sentences[0]) if sentences else 0
        left, right = 0, 1
        for i, sentence in enumerate(sentences[1:], 1):
            if cur_chunk_len + len(sentence) > char_chunk_size:
                chunks.append("".join(sentences[left:right]))
                cur_chunk_len, left = locate_overlap_start_index(left, right)
            cur_chunk_len += len(sentence)
            right = i + 1
        if cur_chunk_len > char_overlap_size:
            chunks.append("".join(sentences[left:]))
        return chunks

    @property
    def doc_type(self) -> DocumentType:
        return DocumentType.text
