from fastmcp import FastMCP
from adventureworks.adventureworks_api import AdventureworksAPI


class AdventureWorksMCP:
    def __init__(self):
        self.api_instance = AdventureworksAPI()
        # Expose the app instance for uvicorn
        fastapi_app = self.api_instance.app
        self.mcp = FastMCP.from_fastapi(app=fastapi_app)
        self._register_tools()

    def _register_tools(self):
        @self.mcp.tool
        def query_order_analyzer(question: str) -> dict:
            """
            Query the order management system with a question
            related to customers suppliers, purchase and sales orders,
            delayed orders and other questions related to orders.

            Args:
                question (str): The question to ask the order analyzer.

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

    def run(self, host="0.0.0.0", port=8088, debug=True, transport="http"):
        self.mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    mcp_instance = AdventureWorksMCP()
    mcp_instance.run(transport="sse",
                     host="0.0.0.0",
                     port=8088,
                     debug=True)
