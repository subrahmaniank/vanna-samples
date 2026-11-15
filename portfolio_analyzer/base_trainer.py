from pathlib import Path
from shared.env_loader import EnvironmentLoader
from shared.qdrant_agent_memory import QdrantAgentMemory
from shared.memory_seeder import MemorySeederBridge


class BaseTrainer:
    """
    Base trainer for Portfolio Analyzer, backed by Vanna 2.0 QdrantAgentMemory.
    Provides get_vn() returning a bridge that routes training into Qdrant.
    """

    def __init__(self, collection_prefix: str = "fsi"):
        env_vars = EnvironmentLoader.load_environment_variables(
            module_path=Path(__file__).parent,
            default_db_name="SEI_DEMO"
        )
        self.memory = QdrantAgentMemory(
            qdrant_url=env_vars.get("qdrant_url") or "http://localhost:6333",
            qdrant_api_key=env_vars.get("qdrant_api_key"),
            collection_prefix=collection_prefix
        )
        self.vn = MemorySeederBridge(self.memory)

    def get_vn(self):
        return self.vn
