from pathlib import Path
from shared.env_loader import EnvironmentLoader
from shared.vector_store_factory import create_agent_memory
from shared.memory_seeder import MemorySeederBridge


class BaseTrainer:
    """
    Base trainer for AdventureWorks, backed by Vanna 2.0 AgentMemory
    (supporting Qdrant, ChromaDB, and FAISS via configuration).
    Provides get_vn() returning a bridge that routes training into the vector store.
    """

    def __init__(self, collection_prefix: str = "aw"):
        env_vars = EnvironmentLoader.load_environment_variables(
            module_path=Path(__file__).parent,
            default_db_name="ADVENTUREWORKS"
        )
        self.memory = create_agent_memory(env_vars, collection_prefix=collection_prefix)
        self.vn = MemorySeederBridge(self.memory)

    def get_vn(self):
        return self.vn
