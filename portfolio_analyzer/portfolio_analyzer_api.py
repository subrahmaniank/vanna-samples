"""
Vanna 2.0 API Entry Point for Portfolio Analyzer.
Migrated to VannaFastAPIServer exposing the app instance for uvicorn.
"""
from portfolio_analyzer.portfolio_analyzer_server import app, run, agent, server

if __name__ == "__main__":
    run(host="0.0.0.0", port=8082)
