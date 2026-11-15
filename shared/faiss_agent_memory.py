import asyncio
import datetime
import json
import os
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

from shared.qdrant_agent_memory import SimpleEmbeddingProvider

try:
    from vanna.capabilities.agent_memory import (
        AgentMemory,
        ToolMemory,
        TextMemory,
        ToolMemorySearchResult,
        TextMemorySearchResult
    )
    from vanna.core.tool import ToolContext
except ImportError:
    from pydantic import BaseModel

    class ToolMemory(BaseModel):
        id: str
        question: str
        tool_name: str
        args: Dict[str, Any]
        success: bool = True
        created_at: str
        metadata: Optional[Dict[str, Any]] = None

    class TextMemory(BaseModel):
        id: str
        content: str
        created_at: str
        metadata: Optional[Dict[str, Any]] = None

    class ToolMemorySearchResult(BaseModel):
        memory: ToolMemory
        score: float

    class TextMemorySearchResult(BaseModel):
        memory: TextMemory
        score: float

    class ToolContext:
        pass

    class AgentMemory:
        pass


class FaissAgentMemory(AgentMemory):
    """
    Native Vanna 2.0 AgentMemory backed by FAISS (Facebook AI Similarity Search).
    Supports persistent disk storage and high-speed in-memory vector retrieval.
    """

    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_prefix: str = "vanna",
        embedding_provider: Optional[SimpleEmbeddingProvider] = None,
    ):
        self.persist_dir = Path(persist_directory) if persist_directory else None
        self.collection_prefix = collection_prefix
        self.embedding = embedding_provider or SimpleEmbeddingProvider()
        self.dimension = self.embedding.dimension

        self.tool_payloads: List[Dict[str, Any]] = []
        self.text_payloads: List[Dict[str, Any]] = []
        self.tool_vectors: List[List[float]] = []
        self.text_vectors: List[List[float]] = []

        self._has_faiss = False
        try:
            import faiss
            self.faiss = faiss
            self._has_faiss = True
            self.tool_index = faiss.IndexFlatIP(self.dimension)
            self.text_index = faiss.IndexFlatIP(self.dimension)
        except ImportError:
            self.faiss = None
            self.tool_index = None
            self.text_index = None

        if self.persist_dir:
            self.persist_dir.mkdir(parents=True, exist_ok=True)
            self._load_from_disk()

    def _normalize(self, vec: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vec)
        if norm == 0:
            return vec
        return vec / norm

    def _save_to_disk(self):
        if not self.persist_dir:
            return
        meta_tool = self.persist_dir / f"{self.collection_prefix}_tool_meta.json"
        meta_text = self.persist_dir / f"{self.collection_prefix}_text_meta.json"
        with open(meta_tool, "w", encoding="utf-8") as f:
            json.dump({"payloads": self.tool_payloads, "vectors": self.tool_vectors}, f)
        with open(meta_text, "w", encoding="utf-8") as f:
            json.dump({"payloads": self.text_payloads, "vectors": self.text_vectors}, f)

    def _load_from_disk(self):
        if not self.persist_dir:
            return
        meta_tool = self.persist_dir / f"{self.collection_prefix}_tool_meta.json"
        meta_text = self.persist_dir / f"{self.collection_prefix}_text_meta.json"
        if meta_tool.exists():
            try:
                with open(meta_tool, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tool_payloads = data.get("payloads", [])
                    self.tool_vectors = data.get("vectors", [])
                    if self._has_faiss and self.tool_vectors:
                        arr = np.array([self._normalize(np.array(v, dtype=np.float32)) for v in self.tool_vectors])
                        self.tool_index = self.faiss.IndexFlatIP(self.dimension)
                        self.tool_index.add(arr)
            except Exception:
                pass

        if meta_text.exists():
            try:
                with open(meta_text, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.text_payloads = data.get("payloads", [])
                    self.text_vectors = data.get("vectors", [])
                    if self._has_faiss and self.text_vectors:
                        arr = np.array([self._normalize(np.array(v, dtype=np.float32)) for v in self.text_vectors])
                        self.text_index = self.faiss.IndexFlatIP(self.dimension)
                        self.text_index.add(arr)
            except Exception:
                pass

    async def save_tool_usage(
        self,
        question: str,
        tool_name: str,
        args: Dict[str, Any],
        context: Optional[ToolContext] = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        def _sync_save():
            mem_id = str(uuid.uuid4())
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            raw_vec = self.embedding.embed_query(question)
            vec = self._normalize(np.array(raw_vec, dtype=np.float32))

            payload = {
                "id": mem_id,
                "question": question,
                "tool_name": tool_name,
                "args": args,
                "success": success,
                "created_at": now,
                "metadata": metadata or {}
            }
            self.tool_payloads.append(payload)
            self.tool_vectors.append([float(x) for x in raw_vec])

            if self._has_faiss:
                self.tool_index.add(np.array([vec], dtype=np.float32))

            self._save_to_disk()

        await asyncio.to_thread(_sync_save)

    async def save_text_memory(
        self,
        content: str,
        context: Optional[ToolContext] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> TextMemory:
        def _sync_save() -> TextMemory:
            mem_id = str(uuid.uuid4())
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            raw_vec = self.embedding.embed_query(content)
            vec = self._normalize(np.array(raw_vec, dtype=np.float32))

            payload = {
                "id": mem_id,
                "memory_id": mem_id,
                "content": content,
                "created_at": now,
                "timestamp": now,
                "metadata": metadata or {}
            }
            self.text_payloads.append(payload)
            self.text_vectors.append([float(x) for x in raw_vec])

            if self._has_faiss:
                self.text_index.add(np.array([vec], dtype=np.float32))

            self._save_to_disk()
            return TextMemory(
                memory_id=mem_id,
                content=content,
                timestamp=now
            )

        return await asyncio.to_thread(_sync_save)

    async def search_similar_usage(
        self,
        question: str,
        context: Optional[ToolContext] = None,
        *,
        limit: int = 10,
        similarity_threshold: float = 0.7,
        tool_name_filter: Optional[str] = None
    ) -> List[ToolMemorySearchResult]:
        def _sync_search() -> List[ToolMemorySearchResult]:
            if not self.tool_payloads:
                return []

            raw_query = self.embedding.embed_query(question)
            query_vec = self._normalize(np.array(raw_query, dtype=np.float32))

            candidates = []
            if self._has_faiss and self.tool_index.ntotal > 0:
                k = min(limit * 2, self.tool_index.ntotal)
                distances, indices = self.tool_index.search(np.array([query_vec]), k)
                for score, idx in zip(distances[0], indices[0]):
                    if idx < 0 or idx >= len(self.tool_payloads):
                        continue
                    if score < similarity_threshold:
                        continue
                    p = self.tool_payloads[idx]
                    if not p.get("success", True):
                        continue
                    if tool_name_filter and p.get("tool_name") != tool_name_filter:
                        continue
                    candidates.append((float(score), p))
                    if len(candidates) >= limit:
                        break
            else:
                # NumPy fallback
                for p, v in zip(self.tool_payloads, self.tool_vectors):
                    if not p.get("success", True):
                        continue
                    if tool_name_filter and p.get("tool_name") != tool_name_filter:
                        continue
                    v_norm = self._normalize(np.array(v, dtype=np.float32))
                    score = float(np.dot(query_vec, v_norm))
                    if score >= similarity_threshold:
                        candidates.append((score, p))

                candidates.sort(key=lambda x: x[0], reverse=True)
                candidates = candidates[:limit]

            results: List[ToolMemorySearchResult] = []
            for rank_idx, (score, p) in enumerate(candidates, start=1):
                mem = ToolMemory(
                    memory_id=str(p.get("memory_id", p.get("id"))),
                    question=p.get("question", ""),
                    tool_name=p.get("tool_name", ""),
                    args=p.get("args", {}),
                    success=p.get("success", True),
                    timestamp=p.get("timestamp", p.get("created_at", "")),
                    metadata=p.get("metadata", {})
                )
                results.append(ToolMemorySearchResult(
                    memory=mem,
                    similarity_score=score,
                    rank=rank_idx
                ))

            return results

        return await asyncio.to_thread(_sync_search)

    async def search_text_memories(
        self,
        query: str,
        context: Optional[ToolContext] = None,
        *,
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[TextMemorySearchResult]:
        def _sync_search() -> List[TextMemorySearchResult]:
            if not self.text_payloads:
                return []

            raw_query = self.embedding.embed_query(query)
            query_vec = self._normalize(np.array(raw_query, dtype=np.float32))

            candidates = []
            if self._has_faiss and self.text_index.ntotal > 0:
                k = min(limit, self.text_index.ntotal)
                distances, indices = self.text_index.search(np.array([query_vec]), k)
                for score, idx in zip(distances[0], indices[0]):
                    if idx < 0 or idx >= len(self.text_payloads):
                        continue
                    if score < similarity_threshold:
                        continue
                    candidates.append((float(score), self.text_payloads[idx]))
            else:
                for p, v in zip(self.text_payloads, self.text_vectors):
                    v_norm = self._normalize(np.array(v, dtype=np.float32))
                    score = float(np.dot(query_vec, v_norm))
                    if score >= similarity_threshold:
                        candidates.append((score, p))

                candidates.sort(key=lambda x: x[0], reverse=True)
                candidates = candidates[:limit]

            results: List[TextMemorySearchResult] = []
            for rank_idx, (score, p) in enumerate(candidates, start=1):
                mem = TextMemory(
                    memory_id=str(p.get("memory_id", p.get("id"))),
                    content=p.get("content", ""),
                    timestamp=p.get("timestamp", p.get("created_at", ""))
                )
                results.append(TextMemorySearchResult(
                    memory=mem,
                    similarity_score=score,
                    rank=rank_idx
                ))

            return results

        return await asyncio.to_thread(_sync_search)

    async def get_recent_memories(
        self,
        context: Optional[ToolContext] = None,
        limit: int = 10
    ) -> List[ToolMemory]:
        res = []
        for p in reversed(self.tool_payloads[-limit:]):
            res.append(ToolMemory(
                memory_id=str(p.get("memory_id", p.get("id"))),
                question=p.get("question", ""),
                tool_name=p.get("tool_name", ""),
                args=p.get("args", {}),
                success=p.get("success", True),
                timestamp=p.get("timestamp", p.get("created_at", "")),
                metadata=p.get("metadata", {})
            ))
        return res

    async def get_recent_text_memories(
        self,
        context: Optional[ToolContext] = None,
        limit: int = 10
    ) -> List[TextMemory]:
        res = []
        for p in reversed(self.text_payloads[-limit:]):
            res.append(TextMemory(
                memory_id=str(p.get("memory_id", p.get("id"))),
                content=p.get("content", ""),
                timestamp=p.get("timestamp", p.get("created_at", ""))
            ))
        return res

    async def delete_by_id(self, context: Optional[ToolContext], memory_id: str) -> bool:
        self.tool_payloads = [p for p in self.tool_payloads if p.get("id") != memory_id]
        self._save_to_disk()
        return True

    async def delete_text_memory(self, context: Optional[ToolContext], memory_id: str) -> bool:
        self.text_payloads = [p for p in self.text_payloads if p.get("id") != memory_id]
        self._save_to_disk()
        return True

    async def clear_memories(
        self,
        context: Optional[ToolContext] = None,
        tool_name: Optional[str] = None,
        before_date: Optional[str] = None
    ) -> int:
        self.tool_payloads.clear()
        self.tool_vectors.clear()
        self.text_payloads.clear()
        self.text_vectors.clear()
        if self._has_faiss:
            self.tool_index = self.faiss.IndexFlatIP(self.dimension)
            self.text_index = self.faiss.IndexFlatIP(self.dimension)
        self._save_to_disk()
        return 1

    # Alias for backwards-compatibility
    clear = clear_memories
