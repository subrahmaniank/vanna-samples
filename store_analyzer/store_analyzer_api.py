"""
Vanna 2.0 API Entry Point for Store Analyzer.
Migrated to VannaFastAPIServer exposing the app instance for uvicorn.
"""
from store_analyzer.store_analyzer_server import app, run, agent, server

if __name__ == "__main__":
    run(host="0.0.0.0", port=8081)
