from typing import Callable, Type

from ..document import Document, DocumentPart, ImagePart, TextPart
from ..utils import Registry, import_submodules
from .config import RerankerConfig
from .reranker import Reranker

__all__ = [
    "AutoReranker",
    "Document",
    "DocumentPart",
    "ImagePart",
    "Reranker",
    "RerankerConfig",
    "TextPart",
]


class AutoReranker(Registry):
    _registry: dict[str, Callable[[], Reranker]] = {}

    @classmethod
    def key_type(cls) -> Type[str]:
        return str

    @classmethod
    def base_class(cls) -> Type[Reranker]:
        return Reranker

    @classmethod
    def get_class(cls, key: str, default=None) -> Type[Reranker]:
        get_func = cls._registry.get(key)
        return get_func() if get_func is not None else default

    @classmethod
    def from_config(cls, class_config: RerankerConfig) -> Reranker | None:
        class_type = cls.get_class(class_config.type)
        if class_type is None:
            raise ValueError(
                f"Reranker type '{class_config.type}' not found.\nAvailable types:\n{cls.get_all_keys()}"
            )
        else:
            return class_type(class_config)


import_submodules(submodule_path=__file__)
