import asyncio
import re
from typing import Dict, Any, Optional
import pandas as pd

try:
    from vanna.capabilities.sql_runner import SqlRunner, RunSqlToolArgs
    from vanna.core.tool import ToolContext
except ImportError:
    class SqlRunner:
        pass
    class RunSqlToolArgs:
        sql: str
    class ToolContext:
        pass


class DuckDbRunner(SqlRunner):
    """
    Executes SQL queries against a DuckDB database (local file, in-memory, or MotherDuck)
    and returns results as pandas DataFrames, compliant with Vanna 2.0 SqlRunner interface.
    """

    def __init__(
        self,
        database_path: str = ":memory:",
        read_only: bool = False,
        config: Optional[Dict[str, Any]] = None
    ):
        self.database_path = database_path or ":memory:"
        self.read_only = read_only
        self.config = config or {}

    def _get_connection(self):
        try:
            import duckdb
        except ImportError:
            raise RuntimeError(
                "duckdb package is required to use DuckDbRunner. "
                "Install it with: pip install duckdb"
            )
        conn = duckdb.connect(
            database=self.database_path,
            read_only=self.read_only,
            config=self.config
        )
        # Configure search_path to discover tables across all schemas without requiring schema prefix
        try:
            schemata = conn.execute(
                "SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog')"
            ).fetchall()
            if schemata:
                schema_names = [s[0] for s in schemata if s[0]]
                for def_s in ["public", "main"]:
                    if def_s not in schema_names:
                        schema_names.append(def_s)
                search_path = ",".join(schema_names)
                conn.execute(f"SET search_path = '{search_path}'")
        except Exception:
            pass
        return conn

    def _execute_query_sync(self, sql: str) -> pd.DataFrame:
        cleaned_sql = sql.strip().rstrip(";")
        # Normalize T-SQL square brackets [col] or [schema].[table] to ANSI double quotes "col"
        cleaned_sql = re.sub(r"\[([^\]\r\n]+)\]", r'"\1"', cleaned_sql)
        # Normalize T-SQL SELECT TOP n to LIMIT n if applicable
        top_match = re.search(r"(?i)^\s*SELECT\s+TOP\s+(\d+)\s+", cleaned_sql)
        if top_match:
            limit_n = top_match.group(1)
            cleaned_sql = re.sub(r"(?i)^\s*SELECT\s+TOP\s+\d+\s+", "SELECT ", cleaned_sql)
            if not re.search(r"(?i)\bLIMIT\s+\d+\b", cleaned_sql):
                cleaned_sql = f"{cleaned_sql} LIMIT {limit_n}"

        conn = self._get_connection()
        try:
            rel = conn.execute(cleaned_sql)
            if rel.description is not None:
                return rel.df()
            else:
                return pd.DataFrame({"rows_affected": [conn.rowcount]})
        finally:
            conn.close()

    async def run_sql(self, args: RunSqlToolArgs, context: ToolContext) -> pd.DataFrame:
        """
        Execute DuckDB SQL query asynchronously via thread pool.
        """
        sql_to_run = getattr(args, "sql", None) or (args.get("sql") if isinstance(args, dict) else str(args))
        return await asyncio.to_thread(self._execute_query_sync, sql_to_run)
