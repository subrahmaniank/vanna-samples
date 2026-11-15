try:
    from fastmcp import FastMCP
except (ImportError, AttributeError):
    from mcp.server.fastmcp import FastMCP
from portfolio_analyzer.agent_factory import create_agent

try:
    from vanna.core.user import RequestContext
except ImportError:
    RequestContext = None


class PortfolioAnalyzerMCP:
    """
    Model Context Protocol (MCP) server for Portfolio Analyzer,
    powered by Vanna 2.0 Agent.
    """

    def __init__(self):
        self.agent = create_agent()
        self.mcp = FastMCP(name="Portfolio Analyzer")
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        async def query_portfolio_analyzer(question: str) -> dict:
            """
            Query the portfolio analyzer with a question
            related to investments, assets, funds, scrips,
            portfolios, accounts, and other financial queries.

            Args:
                question (str): The question to ask the portfolio analyzer.

            Returns:
                dict: The response containing the question and answer from the agent.
            """
            context = RequestContext() if RequestContext else None
            collected_text = []

            async for component in self.agent.send_message(context, question):
                if hasattr(component, "simple_component") and component.simple_component:
                    collected_text.append(str(getattr(component.simple_component, "text", "")))
                elif hasattr(component, "text"):
                    collected_text.append(str(component.text))

            return {
                "question": question,
                "response": "\n".join(collected_text)
            }

    def run(self, host: str = "0.0.0.0", port: int = 8088, transport: str = "sse", debug: bool = True):
        self.mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    mcp_instance = PortfolioAnalyzerMCP()
    mcp_instance.run(transport="sse", host="0.0.0.0", port=8088)
