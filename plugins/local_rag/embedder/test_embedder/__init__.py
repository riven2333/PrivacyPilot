from typing import Type

from .. import AutoEmbedder, Embedder

__all__ = ["get_test_embedder_class"]


@AutoEmbedder.register("test")
def get_test_embedder_class() -> Type[Embedder]:
    from .test_embedder import TestEmbedder

    return TestEmbedder
