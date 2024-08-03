from pathlib import Path

from pydantic import BaseModel

from plugins.local_rag import LocalRAG, clear_local_rag_cache

__all__ = ["RAGRequest", "RAGResponse", "clear_local_rag_cache", "get_rag_engine"]

default_config_path = str(
    Path(__file__).parent.parent.resolve() / "configs" / "local_rag.json"
)


class RAGRequest(BaseModel):
    query: str


class RAGResponse(BaseModel):
    status: str
    message: str
    results: list[str | dict]


def get_rag_engine(config_path: str = default_config_path) -> LocalRAG:
    return LocalRAG(config_path)
