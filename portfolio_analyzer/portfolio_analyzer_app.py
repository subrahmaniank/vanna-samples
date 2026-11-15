"""
Vanna 2.0 Web Application Entry Point for Portfolio Analyzer.
Migrated from VannaFlaskApp to VannaFastAPIServer.
"""
from portfolio_analyzer.portfolio_analyzer_server import run, server, app

if __name__ == "__main__":
    run(host="0.0.0.0", port=8085)
