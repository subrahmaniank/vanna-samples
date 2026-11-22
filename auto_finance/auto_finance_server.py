"""Web and API server for the auto finance Vanna agent (port 8090)."""

from auto_finance.agent_factory import create_agent
from vanna.servers.fastapi import VannaFastAPIServer

agent = create_agent()
server = VannaFastAPIServer(agent)
app = server.create_app()


def run(host: str = "0.0.0.0", port: int = 8090):
    server.run(host=host, port=port)


if __name__ == "__main__":
    run()
