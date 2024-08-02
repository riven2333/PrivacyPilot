from typing import Type

from .. import AutoEmbedder, Embedder

__all__ = ["get_flag_bge_m3_embedder_class"]


@AutoEmbedder.register("flag_bge_m3")
def get_flag_bge_m3_embedder_class() -> Type[Embedder]:
    from .flag_bge_m3_embedder import FlagBGEM3Embedder

    return FlagBGEM3Embedder
