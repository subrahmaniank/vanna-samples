"""Auto finance SQL and chart tools with reliable CSV handoff."""

import re

from vanna.tools import RunSqlTool
from vanna.capabilities.sql_runner import RunSqlToolArgs
from vanna.core.tool import ToolContext, ToolResult

from shared.chart_generator import EnhancedVisualizeDataTool


class AutoFinanceRunSqlTool(RunSqlTool):
    async def execute(self, context: ToolContext, args: RunSqlToolArgs) -> ToolResult:
        sql = args.sql.strip().rstrip(";")
        if re.match(r"^WITH\b", sql, flags=re.IGNORECASE):
            # Vanna's RunSqlTool writes a CSV only when the statement starts
            # with SELECT. A read-only CTE returning rows needs the same path.
            args = args.model_copy(update={"sql": f"SELECT * FROM ({sql}) AS query_result"})
        return await super().execute(context, args)


class AutoFinanceVisualizeDataTool(EnhancedVisualizeDataTool):
    @property
    def description(self) -> str:
        return (
            super().description + " Use only the exact CSV filename returned by "
            "a successful run_sql call in this conversation. Never invent a filename."
        )
