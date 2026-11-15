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


class SnowflakeRunner(SqlRunner):
    """
    Executes SQL queries against a Snowflake data warehouse and returns
    results as pandas DataFrames, compliant with Vanna 2.0 SqlRunner interface.
    """

    def __init__(
        self,
        account: str,
        user: str,
        password: str,
        database: str,
        schema: str = "PUBLIC",
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        **kwargs
    ):
        self.account = account
        self.user = user
        self.password = password
        self.database = database
        self.schema = schema
        self.warehouse = warehouse
        self.role = role
        self.extra_kwargs = kwargs

    def _get_connection(self):
        try:
            import snowflake.connector
        except ImportError:
            raise RuntimeError(
                "snowflake-connector-python is required to connect to Snowflake. "
                "Install it with: pip install 'snowflake-connector-python[pandas]'"
            )

        conn_params = {
            "account": self.account,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "schema": self.schema,
        }
        if self.warehouse:
            conn_params["warehouse"] = self.warehouse
        if self.role:
            conn_params["role"] = self.role

        conn_params.update(self.extra_kwargs)
        return snowflake.connector.connect(**conn_params)

    def _execute_query_sync(self, sql: str) -> pd.DataFrame:
        cleaned_sql = sql.strip().rstrip(";")
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(cleaned_sql)
                # fetch_pandas_all() is optimized in snowflake-connector-python with pyarrow
                if hasattr(cursor, "fetch_pandas_all"):
                    try:
                        return cursor.fetch_pandas_all()
                    except Exception:
                        pass

                if cursor.description is not None:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    if not rows:
                        return pd.DataFrame(columns=columns)
                    return pd.DataFrame.from_records(rows, columns=columns)
                else:
                    return pd.DataFrame({"rows_affected": [cursor.rowcount]})

    async def run_sql(self, args: RunSqlToolArgs, context: ToolContext) -> pd.DataFrame:
        """
        Execute Snowflake SQL query asynchronously via thread pool.
        """
        sql_to_run = getattr(args, "sql", None) or (args.get("sql") if isinstance(args, dict) else str(args))
        return await asyncio.to_thread(self._execute_query_sync, sql_to_run)
