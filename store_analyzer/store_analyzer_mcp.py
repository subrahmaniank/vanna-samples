from fastmcp import FastMCP
from store_analyzer.store_analyzer_api import StoreAnalyzerAPI


class StoreAnalyzerMCP:
    def __init__(self):
        self.api_instance = StoreAnalyzerAPI()
        # Expose the app instance for uvicorn
        fastapi_app = self.api_instance.app
        self.mcp = FastMCP.from_fastapi(app=fastapi_app)
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool
        def query_store_analyzer(question: str) -> dict:
            """
            Query the store analyzer with a question
            related to stores, staff, rental, movies, actors,
            customers and other queries related to dvd rentals.

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

    def run(self, host="0.0.0.0", port=8086, debug=True, transport="http"):
        self.mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    mcp_instance = StoreAnalyzerMCP()
    mcp_instance.run(transport="sse",
                     host="0.0.0.0",
                     port=8086,
                     debug=True)
