import re

from .. import Document, DocumentParser, DocumentParserConfig, DocumentType, TextPart

__all__ = ["TextDocumentParser"]


class TextDocumentParser(DocumentParser):
    def __init__(self, config: DocumentParserConfig) -> None:
        self._config = config
        self._char_chunk_size = config.char_chunk_size
        self._char_overlap_size = config.char_overlap_size
        self._abbreviation_pattern = self.get_abbreviation_pattern()
        self._sentence_endings_pattern = self.get_sentence_endings_pattern()
        self._special_forms_pattern = self.compile_special_forms_pattern()

    @staticmethod
    def get_abbreviation_pattern() -> re.Pattern:
        abbreviations = [
            r"\betc\.",
            r"\bet al\.",
            r"\bi\.e\.",
            r"\be\.g\.",
            r"\bDr\.",
            r"\bMr\.",
            r"\bMrs\.",
            r"\bProf\.",
            r"\bInc\.",
            r"\bLtd\.",
            r"\bCo\.",
            r"\bJr\.",
            r"\bSr\.",
            r"\bvs\.",
            r"\bSt\.",
            r"\bMt\.",
            r"\bMs\.",
            r"\bJan\.",
            r"\bFeb\.",
            r"\bMar\.",
            r"\bApr\.",
            r"\bJun\.",
            r"\bJul\.",
            r"\bAug\.",
            r"\bSep\.",
            r"\bOct\.",
            r"\bNov\.",
            r"\bDec\.",
        ]
        pattern = re.compile("|".join(abbreviations))
        return pattern

    @staticmethod
    def get_sentence_endings_pattern() -> re.Pattern:
        pattern = re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?!。？！])\s")
        return pattern

    @staticmethod
    def compile_special_forms_pattern() -> re.Pattern:
        def get_variations(
            base_pattern: str, prefixes: list[str], suffixes: list[str]
        ) -> str:
            prefixes = [prefix for prefix in prefixes if prefix]
            suffixes = [suffix for suffix in suffixes if suffix]
            if not prefixes and not suffixes:
                return base_pattern
            else:
                prefixes = prefixes if prefixes else [""]
                suffixes = prefixes if prefixes else [""]
                return "|".join(
                    [
                        f"{prefix}{base_pattern}{suffix}"
                        for prefix in prefixes
                        for suffix in suffixes
                    ]
                )

        chapter_pattern_zh_part = "|".join(
            [
                get_variations(
                    r"第?\s*[0-9〇零一二三四五六七八九十百千]+\s*[章节][、\.]?\s*\n",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                )
            ]
        )
        list_item_pattern_zh_part = "|".join(
            [
                get_variations(
                    r"[〇零一二三四五六七八九十百千]+[、\.]?\s",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                )
            ]
        )
        chapter_pattern_en_part = "|".join(
            [
                get_variations(
                    r"[A-Z][a-z]*\s+[A-Z][a-z]*\s*\n",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                ),
                get_variations(
                    r"[A-Z][a-z]*\s+[0-9]+\.?\s*\n",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                ),
                get_variations(
                    r"(?:[0-9]+[\.-])*[0-9]*\s*[A-Z][A-Za-z]*\s*\n",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                ),
            ]
        )
        list_item_pattern_en_part = "|".join(
            [
                get_variations(
                    r"(?:[0-9]+[\.-])*[0-9]+\.?\s",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                ),
                get_variations(
                    r"[\[\(]?(?:[0-9]+[\.-])*[0-9]+[\)\]]?\.?\s",
                    prefixes=[r"^\s*", r"\n+\s*"],
                    suffixes=[],
                ),
            ]
        )
        pattern = re.compile(
            rf"({chapter_pattern_zh_part}|"
            rf"{list_item_pattern_zh_part}|"
            rf"{chapter_pattern_en_part}|"
            rf"{list_item_pattern_en_part})"
        )
        return pattern

    def parse(self, document: Document) -> Document:
        sentences = self._split_sentences(document.parts[0].get_data())
        chunks = self._chunk_sentences(sentences)
        document.parts = [TextPart(chunk) for chunk in chunks]
        return document

    def _split_sentences(self, text: str) -> list[str]:
        text = self._abbreviation_pattern.sub(lambda m: m.group()[:-1], text)

        sentences = self._sentence_endings_pattern.split(text)

        sentences = self._handle_special_forms(sentences, self._special_forms_pattern)
        return sentences

    @staticmethod
    def _handle_special_forms(sentences: list[str], pattern: re.Pattern) -> list[str]:
        new_sentences = []
        for sentence in sentences:
            sub_sentences = pattern.split(sentence)
            for sub_sentence in sub_sentences:
                sub_sentence = sub_sentence.strip()
                if sub_sentence:
                    new_sentences.append(sub_sentence)
        return new_sentences

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
