import asyncio
from typing import Dict, Any, Optional
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    from vanna.capabilities.sql_runner import SqlRunner, RunSqlToolArgs
    from vanna.core.tool import ToolContext
except ImportError:
    # Fallback types for static analysis or standalone execution
    class SqlRunner:
        pass
    class RunSqlToolArgs:
        sql: str
    class ToolContext:
        pass


class PostgresRunner(SqlRunner):
    """
    Executes SQL queries against a PostgreSQL database and returns
    results as pandas DataFrames, compliant with Vanna 2.0 SqlRunner interface.
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        dbname: str = "",
        user: str = "postgres",
        password: str = "",
        sslmode: Optional[str] = None
    ):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.sslmode = sslmode

    def _get_connection(self):
        conn_params = {
            "host": self.host,
            "port": self.port,
            "dbname": self.dbname,
            "user": self.user,
            "password": self.password,
        }
        if self.sslmode:
            conn_params["sslmode"] = self.sslmode
        return psycopg2.connect(**conn_params)

    def _execute_query_sync(self, sql: str) -> pd.DataFrame:
        cleaned_sql = sql.strip().rstrip(";")
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(cleaned_sql)
                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    if not rows:
                        return pd.DataFrame(columns=columns)
                    return pd.DataFrame.from_records(rows, columns=columns)
                else:
                    conn.commit()
                    return pd.DataFrame({"rows_affected": [cursor.rowcount]})

    async def run_sql(self, args: RunSqlToolArgs, context: ToolContext) -> pd.DataFrame:
        """
        Execute SQL query asynchronously via thread pool.
        """
        sql_to_run = getattr(args, "sql", None) or (args.get("sql") if isinstance(args, dict) else str(args))
        return await asyncio.to_thread(self._execute_query_sync, sql_to_run)
