from pathlib import Path
from typing import Optional, Dict, Any

from shared.env_loader import EnvironmentLoader
from shared.snowflake_runner import SnowflakeRunner
from shared.postgres_runner import PostgresRunner
from shared.qdrant_agent_memory import QdrantAgentMemory
from adventureworks.user_resolver import AdventureWorksUserResolver

try:
    from vanna import Agent, AgentConfig
    from vanna.core.agent.config import UiFeatures
    from vanna.core.registry import ToolRegistry
    from vanna.integrations.openai import OpenAILlmService
    from vanna.tools import RunSqlTool
    from vanna.tools.agent_memory import (
        SearchSavedCorrectToolUsesTool,
        SaveQuestionToolArgsTool,
        SaveTextMemoryTool,
    )
except ImportError:
    # Stubs for static verification before vanna is fully loaded
    Agent = None
    AgentConfig = None
    UiFeatures = None
    ToolRegistry = None
    OpenAILlmService = None
    RunSqlTool = None
    SearchSavedCorrectToolUsesTool = None
    SaveQuestionToolArgsTool = None
    SaveTextMemoryTool = None


def create_agent(
    env_vars: Optional[Dict[str, Any]] = None,
    collection_prefix: str = "aw"
) -> Any:
    """
    Factory creating a fully configured Vanna 2.0 Agent for AdventureWorks.
    Uses Snowflake (with Postgres fallback), Qdrant Cloud service, and Azure OpenAI.
    """
    if env_vars is None:
        env_vars = EnvironmentLoader.load_environment_variables(
            module_path=Path(__file__).parent,
            default_db_name="ADVENTUREWORKS"
        )

    # 1. Database Runner (Snowflake preferred, Postgres fallback)
    if env_vars.get("snowflake_account"):
        sql_runner = SnowflakeRunner(
            account=env_vars["snowflake_account"],
            user=env_vars["snowflake_user"],
            password=env_vars["snowflake_password"],
            database=env_vars.get("snowflake_database") or "ADVENTUREWORKS",
            schema=env_vars.get("snowflake_schema") or "PUBLIC",
            warehouse=env_vars.get("snowflake_warehouse") or "COMPUTE_WH",
            role=env_vars.get("snowflake_role"),
        )
    else:
        sql_runner = PostgresRunner(
            host=env_vars["db_host"],
            port=env_vars["db_port"],
            dbname=env_vars["db_name"] or "AdventureWorksOLTP",
            user=env_vars["db_username"],
            password=env_vars["db_password"],
        )

    # 2. Vector Tool Memory (Qdrant Service)
    qdrant_memory = QdrantAgentMemory(
        qdrant_url=env_vars.get("qdrant_url") or "http://localhost:6333",
        qdrant_api_key=env_vars.get("qdrant_api_key"),
        collection_prefix=collection_prefix
    )

    # 3. LLM Service (Azure OpenAI)
    # OpenAILlmService supports base_url for Azure OpenAI endpoints
    azure_endpoint = env_vars.get("azure_openai_endpoint") or None
    if azure_endpoint and not azure_endpoint.endswith("/"):
        azure_endpoint = azure_endpoint + "/"

    llm_service = OpenAILlmService(
        model=env_vars.get("azure_openai_model") or "gpt-4o-mini",
        api_key=env_vars.get("azure_openai_key") or "dummy-key",
        base_url=azure_endpoint,
    ) if OpenAILlmService else None

    # 4. Tool Registry & Permissions
    tool_registry = ToolRegistry() if ToolRegistry else None
    if tool_registry:
        # Register RunSqlTool
        if RunSqlTool:
            tool_registry.register_local_tool(
                RunSqlTool(sql_runner=sql_runner),
                access_groups=["user", "admin"]
            )
        # Register Memory tools
        if SearchSavedCorrectToolUsesTool:
            tool_registry.register_local_tool(
                SearchSavedCorrectToolUsesTool(),
                access_groups=["user", "admin"]
            )
        if SaveQuestionToolArgsTool:
            tool_registry.register_local_tool(
                SaveQuestionToolArgsTool(),
                access_groups=["admin"]
            )
        if SaveTextMemoryTool:
            tool_registry.register_local_tool(
                SaveTextMemoryTool(),
                access_groups=["admin"]
            )

    # 5. User Resolver
    user_resolver = AdventureWorksUserResolver()

    # 6. Agent Configuration & UI Features
    ui_features = UiFeatures(
        feature_group_access={
            "tool_names": ["admin"],
            "tool_arguments": ["admin"],
            "tool_error": ["admin"],
            "tool_invocation_message_in_chat": []
        }
    ) if UiFeatures else None

    agent_config = AgentConfig(
        max_tool_iterations=10,
        stream_responses=True,
        include_thinking_indicators=True,
        ui_features=ui_features
    ) if AgentConfig else None

    if Agent is None:
        raise RuntimeError("Vanna 2.0 is not installed or could not be imported.")

    agent = Agent(
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=qdrant_memory,
        user_resolver=user_resolver,
        config=agent_config
    )
    return agent
