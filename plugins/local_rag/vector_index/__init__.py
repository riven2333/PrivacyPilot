from typing import Callable, Type

from ..document import Document, DocumentPart
from ..utils import Registry, import_submodules
from .config import VectorIndexConfig
from .vector_index import VectorIndex

__all__ = [
    "AutoVectorIndex",
    "Document",
    "DocumentPart",
    "VectorIndex",
    "VectorIndexConfig",
]


class AutoVectorIndex(Registry):
    _registry: dict[str, Callable[[], Type[VectorIndex]]] = {}

    @classmethod
    def key_type(cls) -> Type[str]:
        return str

    @classmethod
    def base_class(cls) -> Type[VectorIndex]:
        return VectorIndex

    @classmethod
    def get_class(cls, key: str, default=None) -> Type[VectorIndex]:
        get_func = cls._registry.get(key)
        return get_func() if get_func is not None else default

    @classmethod
    def from_config(cls, class_config: VectorIndexConfig) -> VectorIndex | None:
        class_type = cls.get_class(class_config.type)
        if class_type is None:
            raise ValueError(
                f"VectorIndex type '{class_config.type}' not found.\nAvailable types:\n{cls.get_all_keys()}"
            )
        else:
            return class_type(class_config)


import_submodules(submodule_path=__file__)
