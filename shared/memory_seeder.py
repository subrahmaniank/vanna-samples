import asyncio
import logging
from typing import Optional, Dict, Any
from shared.qdrant_agent_memory import QdrantAgentMemory

logger = logging.getLogger("MemorySeeder")


class MemorySeederBridge:
    """
    Bridges legacy vn.train() calls into Vanna 2.0 QdrantAgentMemory.
    - DDL and Documentation strings -> stored as text memories in Qdrant
    - SQL queries and (question, SQL) pairs -> stored as tool usage memories in Qdrant
    """

    def __init__(self, agent_memory: QdrantAgentMemory):
        self.memory = agent_memory

    def _run(self, coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(asyncio.run, coro).result()
        else:
            return asyncio.run(coro)

    def train(
        self,
        question: Optional[str] = None,
        sql: Optional[str] = None,
        ddl: Optional[str] = None,
        documentation: Optional[str] = None,
        plan: Optional[str] = None
    ):
        if ddl:
            self._run(self.memory.save_text_memory(content=ddl, metadata={"type": "ddl"}))
        elif documentation:
            self._run(self.memory.save_text_memory(content=documentation, metadata={"type": "documentation"}))
        elif sql:
            q = question or f"Execute query: {sql[:60].strip()}..."
            self._run(self.memory.save_tool_usage(
                question=q,
                tool_name="run_sql",
                args={"sql": sql},
                success=True,
                metadata={"seeded": True}
            ))
