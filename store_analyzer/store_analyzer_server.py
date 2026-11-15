import logging
from typing import List, Any, Optional
from pydantic import BaseModel
from fastapi import Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from store_analyzer.agent_factory import create_agent

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
logger = logging.getLogger("StoreAnalyzerServer")


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
    # Login & Auth endpoints migrating from 1.x SimpleAuthorization
    @app.get("/auth/login", response_class=HTMLResponse)
    async def login_page():
        return """
        <!DOCTYPE html>
        <html>
        <head><title>Sign In - DVD Rental Store</title>
        <style>
            body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #0f172a; color: #fff; }
            .card { background: #1e293b; padding: 2rem; border-radius: 8px; width: 320px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
            input { width: 100%; padding: 0.6rem; margin: 0.5rem 0 1rem; border-radius: 4px; border: 1px solid #475569; background: #334155; color: #fff; box-sizing: border-box; }
            button { width: 100%; padding: 0.7rem; background: #2563eb; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
            button:hover { background: #1d4ed8; }
        </style>
        </head>
        <body>
        <div class="card">
            <h2>DVD Rental Sign In</h2>
            <form action="/auth/login" method="POST">
                <label>Username</label>
                <input type="text" name="user" required autofocus placeholder="admin or hillyer" />
                <label>Password</label>
                <input type="password" name="password" required />
                <button type="submit">Sign In</button>
            </form>
        </div>
        </body>
        </html>
        """

    @app.post("/auth/login")
    async def login(request: Request):
        form_data = await request.form()
        user = str(form_data.get("user", "")).strip()
        password = str(form_data.get("password", "")).strip()
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user", value=user, httponly=False)
        response.set_cookie(key="password", value=password, httponly=False)
        return response

    @app.get("/auth/logout")
    async def logout():
        response = RedirectResponse(url="/auth/login", status_code=303)
        response.delete_cookie(key="user")
        response.delete_cookie(key="password")
        return response

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


def run(host: str = "0.0.0.0", port: int = 8084):
    if server:
        logger.info(f"Starting Store Analyzer Vanna 2.0 Server on http://{host}:{port}")
        server.run(host=host, port=port)
    else:
        import uvicorn
        uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    run(host="0.0.0.0", port=8084)
