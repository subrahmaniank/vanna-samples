"""
Vanna 2.0 Web Application Entry Point for AdventureWorks.
Migrated from VannaFlaskApp to VannaFastAPIServer.
"""
from adventureworks.adventureworks_server import run, server, app

if __name__ == "__main__":
    run(host="0.0.0.0", port=8086)
