from typing import Callable, Type

from ..document import Document, DocumentPart, ImagePart, TextPart
from ..utils import Registry, import_submodules
from .config import EmbedderConfig
from .embedder import Embedder

__all__ = [
    "AutoEmbedder",
    "Document",
    "DocumentPart",
    "Embedder",
    "EmbedderConfig",
    "ImagePart",
    "TextPart",
]


class AutoEmbedder(Registry):
    _registry: dict[str, Callable[[], Type[Embedder]]] = {}

    @classmethod
    def key_type(cls) -> Type[str]:
        return str

    @classmethod
    def base_class(cls) -> Type[Embedder]:
        return Embedder

    @classmethod
    def get_class(cls, key: str, default=None) -> Type[Embedder]:
        get_func = cls._registry.get(key)
        return get_func() if get_func is not None else default

    @classmethod
    def from_config(cls, class_config: EmbedderConfig) -> Embedder | None:
        class_type = cls.get_class(class_config.type)
        if class_type is None:
            raise ValueError(
                f"Embedder type '{class_config.type}' not found.\nAvailable types:\n{cls.get_all_keys()}"
            )
        else:
            return class_type(class_config)


import_submodules(submodule_path=__file__)
