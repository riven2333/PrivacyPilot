from typing import Type

from .. import AutoReranker, Reranker

__all__ = ["get_identity_reranker_class"]


@AutoReranker.register("identity")
def get_identity_reranker_class() -> Type[Reranker]:
    from .identity_reranker import IdentityReranker

    return IdentityReranker
