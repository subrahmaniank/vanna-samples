"""
Vanna 2.0 Web Application Entry Point for Store Analyzer.
Migrated from VannaFlaskApp to VannaFastAPIServer.
"""
from store_analyzer.store_analyzer_server import run, server, app

if __name__ == "__main__":
    run(host="0.0.0.0", port=8084)
