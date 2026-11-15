import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from shared.qdrant_agent_memory import QdrantAgentMemory
from shared.faiss_agent_memory import FaissAgentMemory

try:
    from vanna.capabilities.agent_memory.base import AgentMemory
except ImportError:
    class AgentMemory:
        pass

try:
    from vanna.integrations.chromadb import ChromaAgentMemory
except ImportError:
    ChromaAgentMemory = None

logger = logging.getLogger("VectorStoreFactory")


def create_agent_memory(
    env_vars: Dict[str, Any],
    collection_prefix: str = "vanna",
    default_persist_dir: Optional[str] = None
) -> AgentMemory:
    """
    Factory creating the appropriate AgentMemory instance based on
    VECTOR_STORE in environment variables or detected configuration.

    Supported VECTOR_STORE values:
    - 'qdrant': Qdrant Cloud or local service (uses QDRANT_URL and QDRANT_API_KEY)
    - 'chromadb': ChromaDB local persistent or in-memory vector database
    - 'faiss': FAISS high-performance vector index (local or in-memory)
    """
    store_type = env_vars.get("vector_store", "").strip().lower()
    persist_dir = env_vars.get("vector_persist_dir") or default_persist_dir or f"./{collection_prefix}_vector_store"

    # 1. ChromaDB
    if store_type in ("chromadb", "chroma"):
        logger.info(f"Using ChromaAgentMemory at persist directory: {persist_dir}")
        if ChromaAgentMemory:
            return ChromaAgentMemory(
                persist_directory=persist_dir,
                collection_name=f"{collection_prefix}_tool_memory"
            )
        else:
            raise RuntimeError(
                "chromadb is required for ChromaAgentMemory. Install it with: pip install chromadb"
            )

    # 2. FAISS
    if store_type == "faiss":
        logger.info(f"Using FaissAgentMemory with prefix: {collection_prefix}")
        return FaissAgentMemory(
            persist_directory=persist_dir,
            collection_prefix=collection_prefix
        )

    # 3. Qdrant (explicit or detected via QDRANT_URL)
    if store_type == "qdrant" or (not store_type and env_vars.get("qdrant_url")):
        qdrant_url = env_vars.get("qdrant_url") or "http://localhost:6333"
        logger.info(f"Using QdrantAgentMemory at URL: {qdrant_url} (prefix: {collection_prefix})")
        return QdrantAgentMemory(
            qdrant_url=qdrant_url,
            qdrant_api_key=env_vars.get("qdrant_api_key"),
            collection_prefix=collection_prefix
        )

    # Fallback default: FAISS local/in-memory (no external server required)
    logger.info(f"No specific vector store configured. Defaulting to FaissAgentMemory: {persist_dir}")
    return FaissAgentMemory(
        persist_directory=persist_dir,
        collection_prefix=collection_prefix
    )
