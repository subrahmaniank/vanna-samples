import logging
from typing import List, Any, Optional
from pydantic import BaseModel
from portfolio_analyzer.agent_factory import create_agent

try:
    from vanna.servers.fastapi import VannaFastAPIServer
    from vanna.core.user import RequestContext
except ImportError:
    VannaFastAPIServer = None
    RequestContext = None

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("PortfolioAnalyzerServer")


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    response: str
    sql: Optional[str] = None
    columns: Optional[List[str]] = None
    rows: Optional[List[List[Any]]] = None


agent = create_agent()
server = VannaFastAPIServer(agent) if VannaFastAPIServer else None
app = server.create_app() if server else None

if app:
    @app.post("/v1/query", response_model=QueryResponse)
    async def query(request: QueryRequest):
        logger.info(f"Received query request: {request.question}")
        context = RequestContext() if RequestContext else None
        collected_text = []

        async for component in agent.send_message(context, request.question):
            if hasattr(component, "simple_component") and component.simple_component:
                collected_text.append(str(getattr(component.simple_component, "text", "")))
            elif hasattr(component, "text"):
                collected_text.append(str(component.text))

        return QueryResponse(
            question=request.question,
            response="\n".join(collected_text)
        )


def run(host: str = "0.0.0.0", port: int = 8085):
    if server:
        logger.info(f"Starting Portfolio Analyzer Vanna 2.0 Server on http://{host}:{port}")
        server.run(host=host, port=port)
    else:
        import uvicorn
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run(host="0.0.0.0", port=8085)
