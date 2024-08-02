from typing import Type

from .. import AutoVectorIndex, VectorIndex

__all__ = ["get_faiss_vector_index_class"]


@AutoVectorIndex.register("faiss")
def get_faiss_vector_index_class() -> Type[VectorIndex]:
    from .faiss_vector_index import FaissVectorIndex

    return FaissVectorIndex
