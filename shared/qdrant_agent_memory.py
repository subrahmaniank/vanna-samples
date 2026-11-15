import asyncio
import datetime
import uuid
from typing import Dict, Any, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

try:
    from vanna.capabilities.agent_memory.base import (
        AgentMemory,
        ToolMemory,
        TextMemory,
        ToolMemorySearchResult,
        TextMemorySearchResult
    )
    from vanna.core.tool import ToolContext
except ImportError:
    # Fallback dataclasses if vanna types are not yet resolved
    from pydantic import BaseModel, Field

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


class SimpleEmbeddingProvider:
    """
    Generates embeddings using fastembed (default: BAAI/bge-small-en-v1.5, 384-dim).
    """
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self._model = None
        self.dimension = 384

    def _get_model(self):
        if self._model is None:
            try:
                from fastembed import TextEmbedding
                self._model = TextEmbedding(model_name=self.model_name)
            except Exception as e:
                raise RuntimeError(
                    f"fastembed is required for QdrantAgentMemory embeddings. Error: {e}"
                )
        return self._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        model = self._get_model()
        return [list(vector) for vector in model.embed(texts)]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


class QdrantAgentMemory(AgentMemory):
    """
    Native Vanna 2.0 AgentMemory implementation backed by Qdrant.
    Supports Qdrant Cloud / managed service with API Key and endpoint URL.
    """

    def __init__(
        self,
        qdrant_url: str,
        qdrant_api_key: Optional[str] = None,
        collection_prefix: str = "vanna",
        embedding_provider: Optional[SimpleEmbeddingProvider] = None,
        client: Optional[QdrantClient] = None
    ):
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        self.collection_prefix = collection_prefix
        self.tool_collection = f"{collection_prefix}_tool_memory"
        self.text_collection = f"{collection_prefix}_text_memory"

        self.client = client or QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
            check_compatibility=False,
            timeout=5.0
        )
        self.embedding = embedding_provider or SimpleEmbeddingProvider()
        self._collections_ensured = False

    def _ensure_collections(self):
        """
        Verify that tool and text collections exist; create them if not.
        Lazy execution when first saving or searching.
        """
        if self._collections_ensured:
            return
        try:
            existing = [c.name for c in self.client.get_collections().collections]
            dim = self.embedding.dimension
            for col_name in [self.tool_collection, self.text_collection]:
                if col_name not in existing:
                    try:
                        self.client.create_collection(
                            collection_name=col_name,
                            vectors_config=qmodels.VectorParams(
                                size=dim,
                                distance=qmodels.Distance.COSINE
                            )
                        )
                    except Exception:
                        pass
            self._collections_ensured = True
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
            vector = self.embedding.embed_query(question)

            payload = {
                "id": mem_id,
                "question": question,
                "tool_name": tool_name,
                "args": args,
                "success": success,
                "created_at": now,
                "metadata": metadata or {}
            }

            self.client.upsert(
                collection_name=self.tool_collection,
                points=[
                    qmodels.PointStruct(
                        id=mem_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )

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
            vector = self.embedding.embed_query(content)

            payload = {
                "id": mem_id,
                "content": content,
                "created_at": now,
                "metadata": metadata or {}
            }

            self.client.upsert(
                collection_name=self.text_collection,
                points=[
                    qmodels.PointStruct(
                        id=mem_id,
                        vector=vector,
                        payload=payload
                    )
                ]
            )
            return TextMemory(
                id=mem_id,
                content=content,
                created_at=now,
                metadata=metadata or {}
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
            vector = self.embedding.embed_query(question)
            filter_conditions = [
                qmodels.FieldCondition(
                    key="success",
                    match=qmodels.MatchValue(value=True)
                )
            ]
            if tool_name_filter:
                filter_conditions.append(
                    qmodels.FieldCondition(
                        key="tool_name",
                        match=qmodels.MatchValue(value=tool_name_filter)
                    )
                )

            query_filter = qmodels.Filter(must=filter_conditions)
            hits = self.client.search(
                collection_name=self.tool_collection,
                query_vector=vector,
                query_filter=query_filter,
                limit=limit,
                score_threshold=similarity_threshold
            )

            results = []
            for hit in hits:
                p = hit.payload or {}
                mem = ToolMemory(
                    id=str(p.get("id", hit.id)),
                    question=p.get("question", ""),
                    tool_name=p.get("tool_name", ""),
                    args=p.get("args", {}),
                    success=p.get("success", True),
                    created_at=p.get("created_at", ""),
                    metadata=p.get("metadata", {})
                )
                results.append(ToolMemorySearchResult(memory=mem, score=hit.score))
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
            vector = self.embedding.embed_query(query)
            hits = self.client.search(
                collection_name=self.text_collection,
                query_vector=vector,
                limit=limit,
                score_threshold=similarity_threshold
            )

            results = []
            for hit in hits:
                p = hit.payload or {}
                mem = TextMemory(
                    id=str(p.get("id", hit.id)),
                    content=p.get("content", ""),
                    created_at=p.get("created_at", ""),
                    metadata=p.get("metadata", {})
                )
                results.append(TextMemorySearchResult(memory=mem, score=hit.score))
            return results

        return await asyncio.to_thread(_sync_search)

    async def get_recent_memories(
        self,
        context: Optional[ToolContext] = None,
        limit: int = 10
    ) -> List[ToolMemory]:
        def _sync_get() -> List[ToolMemory]:
            records, _ = self.client.scroll(
                collection_name=self.tool_collection,
                limit=limit,
                with_payload=True
            )
            res = []
            for r in records:
                p = r.payload or {}
                res.append(
                    ToolMemory(
                        id=str(p.get("id", r.id)),
                        question=p.get("question", ""),
                        tool_name=p.get("tool_name", ""),
                        args=p.get("args", {}),
                        success=p.get("success", True),
                        created_at=p.get("created_at", ""),
                        metadata=p.get("metadata", {})
                    )
                )
            return res

        return await asyncio.to_thread(_sync_get)

    async def get_recent_text_memories(
        self,
        context: Optional[ToolContext] = None,
        limit: int = 10
    ) -> List[TextMemory]:
        def _sync_get() -> List[TextMemory]:
            records, _ = self.client.scroll(
                collection_name=self.text_collection,
                limit=limit,
                with_payload=True
            )
            res = []
            for r in records:
                p = r.payload or {}
                res.append(
                    TextMemory(
                        id=str(p.get("id", r.id)),
                        content=p.get("content", ""),
                        created_at=p.get("created_at", ""),
                        metadata=p.get("metadata", {})
                    )
                )
            return res

        return await asyncio.to_thread(_sync_get)

    async def delete_by_id(self, context: Optional[ToolContext], memory_id: str) -> bool:
        def _sync_delete():
            self.client.delete(
                collection_name=self.tool_collection,
                points_selector=qmodels.PointIdsList(points=[memory_id])
            )
            return True

        return await asyncio.to_thread(_sync_delete)

    async def delete_text_memory(self, context: Optional[ToolContext], memory_id: str) -> bool:
        def _sync_delete():
            self.client.delete(
                collection_name=self.text_collection,
                points_selector=qmodels.PointIdsList(points=[memory_id])
            )
            return True

        return await asyncio.to_thread(_sync_delete)

    async def clear(
        self,
        context: Optional[ToolContext] = None,
        tool_name: Optional[str] = None,
        before_date: Optional[str] = None
    ) -> int:
        def _sync_clear():
            # Delete both collections and recreate
            for col in [self.tool_collection, self.text_collection]:
                try:
                    self.client.delete_collection(col)
                except Exception:
                    pass
            self._ensure_collections()
            return 1

        return await asyncio.to_thread(_sync_clear)
