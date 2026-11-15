import logging
from typing import Dict, Any, Optional

from shared.snowflake_runner import SnowflakeRunner
from shared.postgres_runner import PostgresRunner
from shared.duckdb_runner import DuckDbRunner

try:
    from vanna.capabilities.sql_runner import SqlRunner
except ImportError:
    class SqlRunner:
        pass

logger = logging.getLogger("DatabaseFactory")


def create_sql_runner(
    env_vars: Dict[str, Any],
    default_db_name: Optional[str] = None
) -> SqlRunner:
    """
    Factory creating the appropriate SqlRunner instance based on
    DATABASE_TYPE in environment variables or detected connection parameters.

    Supported DATABASE_TYPE values:
    - 'duckdb': DuckDB local file, in-memory, or MotherDuck
    - 'snowflake': Snowflake Data Cloud
    - 'postgres': PostgreSQL database
    """
    db_type = env_vars.get("database_type", "").strip().lower()

    # 1. Explicit DuckDB or detected DuckDB path
    if db_type == "duckdb" or (not db_type and env_vars.get("duckdb_path")):
        duckdb_path = env_vars.get("duckdb_path") or f"{default_db_name or 'database'}.duckdb"
        logger.info(f"Using DuckDbRunner with path: {duckdb_path}")
        return DuckDbRunner(
            database_path=duckdb_path,
            read_only=bool(env_vars.get("duckdb_read_only", False))
        )

    # 2. Explicit Snowflake or detected Snowflake account
    if db_type == "snowflake" or (not db_type and env_vars.get("snowflake_account")):
        logger.info("Using SnowflakeRunner")
        return SnowflakeRunner(
            account=env_vars["snowflake_account"],
            user=env_vars["snowflake_user"],
            password=env_vars["snowflake_password"],
            database=env_vars.get("snowflake_database") or default_db_name or "ADVENTUREWORKS",
            schema=env_vars.get("snowflake_schema") or "PUBLIC",
            warehouse=env_vars.get("snowflake_warehouse") or "COMPUTE_WH",
            role=env_vars.get("snowflake_role"),
        )

    # 3. Explicit Postgres or detected Postgres host
    if db_type == "postgres" or (not db_type and env_vars.get("db_host")):
        logger.info(f"Using PostgresRunner for database: {env_vars.get('db_name') or default_db_name}")
        return PostgresRunner(
            host=env_vars.get("db_host") or "localhost",
            port=int(env_vars.get("db_port") or 5432),
            dbname=env_vars.get("db_name") or default_db_name or "",
            user=env_vars.get("db_username") or "postgres",
            password=env_vars.get("db_password") or "",
        )

    # Fallback default: DuckDB in-memory or named file
    fallback_path = f"{default_db_name or 'vanna'}.duckdb"
    logger.warning(
        f"No specific database configuration detected. Defaulting to DuckDbRunner: {fallback_path}"
    )
    return DuckDbRunner(database_path=fallback_path)
