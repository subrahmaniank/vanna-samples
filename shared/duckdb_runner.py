import asyncio
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
        return duckdb.connect(
            database=self.database_path,
            read_only=self.read_only,
            config=self.config
        )

    def _execute_query_sync(self, sql: str) -> pd.DataFrame:
        cleaned_sql = sql.strip().rstrip(";")
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
