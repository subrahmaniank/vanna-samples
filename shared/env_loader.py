import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from shared.ssl_utils import RelaxedSSLContext


class EnvironmentLoader:
    """
    Loads configuration strictly from the module-level .env file,
    resolving module-local paths for DuckDB database files and vector store persist directories.
    Uses the operating system trust store for outbound HTTPS.
    """

    @staticmethod
    def load_environment_variables(
        module_path: Optional[Path] = None,
        default_db_name: Optional[str] = None
    ) -> Dict[str, Any]:
        # Determine module directory
        if module_path:
            module_dir = module_path if module_path.is_dir() else module_path.parent
        else:
            module_dir = Path.cwd()

        # Load strictly from module-level .env
        module_env = module_dir / ".env"
        if module_env.exists():
            load_dotenv(dotenv_path=module_env, override=True)

        # Configure the system trust store before HTTP clients are created.
        RelaxedSSLContext.configure_ssl()

        # Resolve vector persist dir relative to module folder
        raw_vector_dir = os.getenv("VECTOR_PERSIST_DIR", "").strip() or "./vector_store"
        p_vector = Path(raw_vector_dir)
        if not p_vector.is_absolute():
            vector_persist_dir = str((module_dir / p_vector).resolve())
        else:
            vector_persist_dir = str(p_vector.resolve())

        # Resolve duckdb path relative to module folder
        raw_duckdb_path = os.getenv("DUCKDB_PATH", "").strip()
        if not raw_duckdb_path and default_db_name:
            raw_duckdb_path = f"{default_db_name.lower()}.duckdb"

        if raw_duckdb_path and raw_duckdb_path != ":memory:":
            p_duckdb = Path(raw_duckdb_path)
            if not p_duckdb.is_absolute():
                duckdb_path = str((module_dir / p_duckdb).resolve())
            else:
                duckdb_path = str(p_duckdb.resolve())
        else:
            duckdb_path = raw_duckdb_path

        return {
            # Maximum tool executions allowed for one chat response.
            "max_tool_iterations": int(os.getenv("VANNA_MAX_TOOL_ITERATIONS", "25")),

            # Vector Store Selector: 'qdrant', 'chromadb', 'faiss'
            "vector_store": os.getenv("VECTOR_STORE", "qdrant").strip().lower(),
            "vector_persist_dir": vector_persist_dir,

            # Qdrant Cloud / Managed Service
            "qdrant_url": os.getenv("QDRANT_URL", "").strip(),
            "qdrant_api_key": os.getenv("QDRANT_API_KEY", "").strip() or None,

            # Database Selector: 'duckdb', 'snowflake', 'postgres'
            "database_type": os.getenv("DATABASE_TYPE", "duckdb").strip().lower(),

            # DuckDB Configuration
            "duckdb_path": duckdb_path,
            "duckdb_read_only": os.getenv("DUCKDB_READ_ONLY", "false").lower() in ("true", "1", "yes"),

            # Snowflake Database Configuration
            "snowflake_account": os.getenv("SNOWFLAKE_ACCOUNT", "").strip(),
            "snowflake_user": os.getenv("SNOWFLAKE_USER", "").strip(),
            "snowflake_password": os.getenv("SNOWFLAKE_PASSWORD", "").strip(),
            "snowflake_database": os.getenv("SNOWFLAKE_DATABASE", default_db_name or "").strip(),
            "snowflake_schema": os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC").strip(),
            "snowflake_warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH").strip(),
            "snowflake_role": os.getenv("SNOWFLAKE_ROLE", "").strip() or None,

            # Legacy PostgreSQL parameters (for backwards-compatibility)
            "db_host": os.getenv("POSTGRES_HOST", "localhost").strip(),
            "db_port": int(os.getenv("POSTGRES_PORT", "5432")),
            "db_name": os.getenv("POSTGRES_DATABASE", default_db_name or "").strip(),
            "db_username": os.getenv("POSTGRES_USERNAME", "postgres").strip(),
            "db_password": os.getenv("POSTGRES_PASSWORD", "").strip(),

            # LLM Provider: 'openrouter', 'bedrock_mantle', 'azure_openai', 'openai'
            "llm_provider": os.getenv("LLM_PROVIDER", "").strip().lower(),

            # OpenRouter (Unified API endpoint)
            "openrouter_api_key": os.getenv("OPENROUTER_API_KEY", "").strip() or None,
            "openrouter_model": os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet").strip(),
            "openrouter_base_url": os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").strip(),
            "openrouter_site_url": os.getenv("OPENROUTER_SITE_URL", os.getenv("OR_SITE_URL", "")).strip(),
            "openrouter_app_name": os.getenv("OPENROUTER_APP_NAME", os.getenv("OR_APP_NAME", "Vanna 2.0 SQL Agent")).strip(),

            # AWS Bedrock Mantle Endpoint & Credentials
            "bedrock_mantle_endpoint": os.getenv("BEDROCK_MANTLE_ENDPOINT", os.getenv("AWS_BEDROCK_MANTLE_ENDPOINT", "")).strip(),
            "bedrock_mantle_api_key": os.getenv("BEDROCK_MANTLE_API_KEY", os.getenv("AWS_BEDROCK_API_KEY", "")).strip() or None,
            "bedrock_mantle_model": os.getenv("BEDROCK_MANTLE_MODEL", os.getenv("AWS_BEDROCK_MODEL", "anthropic.claude-3-5-sonnet-20241022-v2:0")).strip(),
            "bedrock_mantle_project_id": os.getenv("BEDROCK_MANTLE_PROJECT_ID", "").strip() or None,
            "bedrock_region": os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")).strip(),

            # Azure OpenAI
            "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "").strip(),
            "azure_openai_key": os.getenv("AZURE_OPENAI_API_KEY", "").strip(),
            "azure_openai_model": os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini").strip(),
            "azure_openai_api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview").strip(),
        }
