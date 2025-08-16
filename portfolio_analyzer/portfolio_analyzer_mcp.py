from fastmcp import FastMCP
from portfolio_analyzer.portfolio_analyzer_api import PortfolioAnalyzerAPI


class PortfolioAnalyzerMCP:
    def __init__(self):
        self.api_instance = PortfolioAnalyzerAPI()
        # Expose the app instance for uvicorn
        fastapi_app = self.api_instance.app
        self.mcp = FastMCP.from_fastapi(app=fastapi_app)
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool
        def query_portfolio_analyzer(question: str) -> dict:
            """
            Query the portfolio analyzer with a question
            related to investments, assets, funds, scrips,
            porfolios, accounts, and other financial queries.

            Args:
                question (str): The question to ask the porfolio analyzer.

            Returns:
                dict: The response from the API containing
                SQL, columns, rows and original question.
            """
            response = self.api_instance.query_vanna(question)
            return {
                "sql": response["sql"],
                "columns": response["columns"],
                "rows": response["rows"],
                "question": response["question"]
            }

    def run(self, host="0.0.0.0", port=8087, debug=True, transport="http"):
        self.mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    mcp_instance = PortfolioAnalyzerMCP()
    mcp_instance.run(transport="sse",
                     host="0.0.0.0",
                     port=8087,
                     debug=True)
