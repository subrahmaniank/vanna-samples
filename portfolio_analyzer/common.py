import os
from dotenv import load_dotenv
import certifi
from qdrant_client import QdrantClient
from vanna.qdrant import Qdrant_VectorStore
from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI


class EnvironmentLoader:
    @staticmethod
    def load_environment_variables():
        load_dotenv()
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

        return {
            "qdrant_url": os.getenv("QDRANT_URL"),
            "qdrant_api_key": os.getenv("QDRANT_API_KEY"),
            "db_host": os.getenv("POSTGRES_HOST"),
            "db_port": os.getenv("POSTGRES_PORT"),
            "db_name": os.getenv("POSTGRES_DATABASE"),
            "db_username": os.getenv("POSTGRES_USERNAME"),
            "db_password": os.getenv("POSTGRES_PASSWORD"),
            "azure_openai_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "azure_openai_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "azure_openai_model": os.getenv("AZURE_OPENAI_MODEL"),
        }


class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(
            self,
            client=AzureOpenAI(
                api_key=config["azure_openai_key"],
                api_version="2024-02-15-preview",
                azure_endpoint=config["azure_openai_endpoint"],
            ),
            config=config,
        )

    @staticmethod
    def create_instance(env_vars):
        return MyVanna(
            config={
                "client": QdrantClient(url=env_vars["qdrant_url"],
                                       api_key=env_vars["qdrant_api_key"]),
                "model": env_vars["azure_openai_model"],
                "documentation_collection_name": "fsi_doc",
                "sql_collection_name": "fsi_sql",
                "ddl_collection_name": "fsi_ddl",
                "azure_openai_key": env_vars["azure_openai_key"],
                "azure_openai_endpoint": env_vars["azure_openai_endpoint"],
            }
        )
