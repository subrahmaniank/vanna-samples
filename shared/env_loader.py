import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from shared.ssl_utils import RelaxedSSLContext


class EnvironmentLoader:
    """
    Loads configuration from module-level or root-level .env files,
    configures SSL context and certificates, and provides environment dict
    for Snowflake, Qdrant Cloud, and Azure OpenAI.
    """

    @staticmethod
    def load_environment_variables(
        module_path: Optional[Path] = None,
        default_db_name: Optional[str] = None
    ) -> Dict[str, Any]:
        # 1. Load root-level .env if present
        root_dir = Path(__file__).resolve().parent.parent
        root_env = root_dir / ".env"
        if root_env.exists():
            load_dotenv(dotenv_path=root_env, override=False)

        # 2. Load module-level .env if specified (takes precedence)
        if module_path:
            module_dir = module_path if module_path.is_dir() else module_path.parent
            module_env = module_dir / ".env"
            if module_env.exists():
                load_dotenv(dotenv_path=module_env, override=True)

        # 3. Configure SSL context and CA bundles
        RelaxedSSLContext.configure_ssl()

        return {
            # Qdrant Cloud / Managed Service
            "qdrant_url": os.getenv("QDRANT_URL", "").strip(),
            "qdrant_api_key": os.getenv("QDRANT_API_KEY", "").strip() or None,

            # Database Selector: 'duckdb', 'snowflake', 'postgres'
            "database_type": os.getenv("DATABASE_TYPE", "").strip().lower(),

            # DuckDB Configuration
            "duckdb_path": os.getenv("DUCKDB_PATH", "").strip(),
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

            # Azure OpenAI
            "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", "").strip(),
            "azure_openai_key": os.getenv("AZURE_OPENAI_API_KEY", "").strip(),
            "azure_openai_model": os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini").strip(),
            "azure_openai_api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview").strip(),
        }
