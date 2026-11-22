"""MCP server for auto finance questions (port 8091)."""

from fastmcp import FastMCP
from vanna.core.user import RequestContext

from auto_finance.agent_factory import create_agent


class AutoFinanceMCP:
    def __init__(self):
        self.agent = create_agent()
        self.mcp = FastMCP(name="Auto Finance Analysis")
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        async def query_auto_finance(question: str) -> dict:
            """Answer a question about originations, portfolio risk, payments, or collections."""
            parts = []
            async for component in self.agent.send_message(RequestContext(), question):
                simple = getattr(component, "simple_component", None)
                if simple:
                    value = getattr(simple, "text", None)
                else:
                    value = getattr(component, "text", None)
                if value:
                    parts.append(str(value))
            return {"question": question, "response": "\n".join(parts)}

    def run(self, host: str = "0.0.0.0", port: int = 8091):
        self.mcp.run(transport="sse", host=host, port=port)


if __name__ == "__main__":
    AutoFinanceMCP().run()
