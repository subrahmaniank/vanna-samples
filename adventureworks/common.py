import sys
import ssl
import warnings
import os
from pathlib import Path
from dotenv import load_dotenv
import certifi
from qdrant_client import QdrantClient
from vanna.qdrant import Qdrant_VectorStore
from vanna.openai import OpenAI_Chat
from openai import AzureOpenAI


class EnvironmentLoader:
    @staticmethod
    def load_environment_variables():
        env_path = Path(__file__).parent / ".env"
        load_dotenv(dotenv_path=env_path)
        os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

        ssl.context = RelaxedSSLContext.create_relaxed_ssl_context()

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
            "azure_openai_api_version": os.getenv("AZURE_OPENAI_API_VERSION")
        }


class MyVanna(Qdrant_VectorStore, OpenAI_Chat):
    def __init__(self, config):
        Qdrant_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(
            self,
            client=AzureOpenAI(
                api_key=config["azure_openai_key"],
                api_version=config["azure_openai_api_version"],
                azure_endpoint=config["azure_openai_endpoint"]
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
                "documentation_collection_name": "aw_doc",
                "sql_collection_name": "aw_sql",
                "ddl_collection_name": "aw_ddl",
                "azure_openai_key": env_vars["azure_openai_key"],
                "azure_openai_endpoint": env_vars["azure_openai_endpoint"],
                "azure_openai_api_version": env_vars["azure_openai_api_version"]
            }
        )


class RelaxedSSLContext:
    @staticmethod
    def create_relaxed_ssl_context(
        purpose=ssl.Purpose.SERVER_AUTH,
        *,
        cafile=None,
        capath=None,
        cadata=None
    ) -> ssl.SSLContext:

        # Create the default SSL context
        ctx = ssl.create_default_context(
            purpose=purpose, cafile=cafile, capath=capath, cadata=cadata
        )

        if sys.version_info >= (3, 13):

            """
            Create an SSL context with relaxed verification flags.
            This reverts Python 3.13's stricter SSL checks.
            Use only if you cannot fix your CA!
            """
            warnings.warn(
                "Disabling VERIFY_X509_STRICT and VERIFY_X509_PARTIAL_CHAIN"
                " in create_default_context().\n"
                "This reverts Python 3.13's stricter SSL checks. "
                "Use only if you cannot fix your CA!"
            )

            # Remove the Python 3.13 flags if they exist
            if hasattr(ssl, "VERIFY_X509_STRICT"):
                ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
            if hasattr(ssl, "VERIFY_X509_PARTIAL_CHAIN"):
                ctx.verify_flags &= ~ssl.VERIFY_X509_PARTIAL_CHAIN

        return ctx
