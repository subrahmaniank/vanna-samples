try:
    from fastmcp import FastMCP
except (ImportError, AttributeError):
    from mcp.server.fastmcp import FastMCP
from store_analyzer.agent_factory import create_agent

try:
    from vanna.core.user import RequestContext
except ImportError:
    RequestContext = None


class StoreAnalyzerMCP:
    """
    Model Context Protocol (MCP) server for Store Analyzer (DVD Rental),
    powered by Vanna 2.0 Agent.
    """

    def __init__(self):
        self.agent = create_agent()
        self.mcp = FastMCP(name="Store Analyzer")
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool()
        async def query_store_analyzer(question: str) -> dict:
            """
            Query the store analyzer with a question
            related to stores, staff, rental, movies, actors,
            customers and other queries related to dvd rentals.

            Args:
                question (str): The question to ask the store analyzer.

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

    def run(self, host: str = "0.0.0.0", port: int = 8087, transport: str = "sse", debug: bool = True):
        self.mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    mcp_instance = StoreAnalyzerMCP()
    mcp_instance.run(transport="sse", host="0.0.0.0", port=8087)
