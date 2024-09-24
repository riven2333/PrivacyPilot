class VectorIndexConfig:
    def __init__(self, vector_index_config: dict) -> None:
        self.type: str = vector_index_config.get("type", "faiss")
        self.dimension: int | None = vector_index_config.get("dimension")
