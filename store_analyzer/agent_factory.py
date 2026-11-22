from pathlib import Path
from typing import Optional, Dict, Any

from shared.env_loader import EnvironmentLoader
from shared.database_factory import create_sql_runner
from shared.vector_store_factory import create_agent_memory
from shared.llm_factory import create_llm_service
from shared.system_prompt_builder import (
    EnhancedSystemPromptBuilder,
    EnhancedVisualizeDataTool,
    STORE_ANALYZER_GUIDELINES,
)
from store_analyzer.user_resolver import StoreAnalyzerUserResolver


try:
    from vanna import Agent, AgentConfig
    from vanna.core.agent.config import UiFeatures
    from vanna.core.registry import ToolRegistry
    from vanna.tools import RunSqlTool, VisualizeDataTool
    from vanna.integrations.local import LocalFileSystem
    from vanna.tools.agent_memory import (
        SearchSavedCorrectToolUsesTool,
        SaveQuestionToolArgsTool,
        SaveTextMemoryTool,
    )
except ImportError:
    Agent = None
    AgentConfig = None
    UiFeatures = None
    ToolRegistry = None
    RunSqlTool = None
    VisualizeDataTool = None
    LocalFileSystem = None
    SearchSavedCorrectToolUsesTool = None
    SaveQuestionToolArgsTool = None
    SaveTextMemoryTool = None



def create_agent(
    env_vars: Optional[Dict[str, Any]] = None,
    collection_prefix: str = "dr"
) -> Any:
    """
    Factory creating a fully configured Vanna 2.0 Agent for Store Analyzer (DVD Rental).
    Supports Snowflake/DuckDB/Postgres, Qdrant/ChromaDB/FAISS, and Bedrock Mantle/Azure/OpenAI.
    """
    if env_vars is None:
        env_vars = EnvironmentLoader.load_environment_variables(
            module_path=Path(__file__).parent,
            default_db_name="DVDRENTAL"
        )

    # 1. Database Runner (Snowflake, DuckDB, or Postgres)
    sql_runner = create_sql_runner(env_vars, default_db_name="DVDRENTAL")

    # 2. Vector Tool Memory (Qdrant, ChromaDB, or FAISS via create_agent_memory)
    agent_memory = create_agent_memory(env_vars, collection_prefix=collection_prefix)

    # 3. LLM Service (AWS Bedrock Mantle, Azure OpenAI, or standard OpenAI)
    llm_service = create_llm_service(env_vars)

    # 4. Local FileSystem for Query Results and Visualizations
    fs_dir = Path(__file__).parent / ".vanna_fs"
    fs_dir.mkdir(parents=True, exist_ok=True)
    file_system = LocalFileSystem(working_directory=fs_dir) if LocalFileSystem else None

    # 5. Tool Registry & Permissions
    tool_registry = ToolRegistry() if ToolRegistry else None
    if tool_registry:
        if RunSqlTool:
            tool_registry.register_local_tool(
                RunSqlTool(sql_runner=sql_runner, file_system=file_system),
                access_groups=["user", "admin"]
            )
        viz_tool_cls = EnhancedVisualizeDataTool if EnhancedVisualizeDataTool else VisualizeDataTool
        if viz_tool_cls:
            tool_registry.register_local_tool(
                viz_tool_cls(file_system=file_system),
                access_groups=["user", "admin"]
            )

        if SearchSavedCorrectToolUsesTool:
            tool_registry.register_local_tool(
                SearchSavedCorrectToolUsesTool(),
                access_groups=["user", "admin"]
            )
        if SaveQuestionToolArgsTool:
            class SaveQuestionToolUsesAlias(SaveQuestionToolArgsTool):
                @property
                def name(self) -> str:
                    return "save_question_tool_uses"

            tool_registry.register_local_tool(
                SaveQuestionToolArgsTool(),
                access_groups=["user", "admin"]
            )
            tool_registry.register_local_tool(
                SaveQuestionToolUsesAlias(),
                access_groups=["user", "admin"]
            )
        if SaveTextMemoryTool:
            tool_registry.register_local_tool(
                SaveTextMemoryTool(),
                access_groups=["user", "admin"]
            )

    # 6. User Resolver with Role Mapping
    user_resolver = StoreAnalyzerUserResolver()

    # 7. Agent Configuration & UI Features
    ui_features = UiFeatures(
        feature_group_access={
            "tool_names": ["admin"],
            "tool_arguments": ["admin"],
            "tool_error": ["admin"],
            "tool_invocation_message_in_chat": []
        }
    ) if UiFeatures else None

    agent_config = AgentConfig(
        max_tool_iterations=int(env_vars.get("max_tool_iterations", 25)),
        stream_responses=True,
        include_thinking_indicators=True,
        ui_features=ui_features
    ) if AgentConfig else None

    # 8. Enhanced System Prompt Builder (Schema qualification & native UI charting)
    system_prompt_builder = EnhancedSystemPromptBuilder(
        db_guidelines=STORE_ANALYZER_GUIDELINES
    )

    if Agent is None:
        raise RuntimeError("Vanna 2.0 is not installed or could not be imported.")

    agent = Agent(
        llm_service=llm_service,
        tool_registry=tool_registry,
        agent_memory=agent_memory,
        user_resolver=user_resolver,
        config=agent_config,
        system_prompt_builder=system_prompt_builder
    )
    return agent

