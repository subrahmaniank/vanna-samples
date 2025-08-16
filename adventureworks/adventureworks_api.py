from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import List, Any
import logging
from adventureworks.common import EnvironmentLoader, MyVanna


class PortfolioAnalyzerAPI:
    def __init__(self):
        self.env_vars = EnvironmentLoader.load_environment_variables()
        self._initialize_vanna()
        self._initialize_app()

    def _initialize_vanna(self):
        self.vn = MyVanna.create_instance(self.env_vars)
        self.vn.connect_to_postgres(
            host=self.env_vars["db_host"],
            port=self.env_vars["db_port"],
            dbname=self.env_vars["db_name"],
            user=self.env_vars["db_username"],
            password=self.env_vars["db_password"]
        )

    def _initialize_app(self):

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format=(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        )
        self.logger = logging.getLogger(__name__)

        @asynccontextmanager
        async def startup_event(app: FastAPI):
            self.logger.info("Starting up the AdventureWorks API")
            try:
                connect_db()
                yield
            finally:
                self.logger.info("Shutting down the AdventureWorks API")

        def connect_db():
            self.logger.info("Connecting to PostgreSQL database")
            self.vn.connect_to_postgres(
                host=self.env_vars["db_host"],
                port=self.env_vars["db_port"],
                dbname=self.env_vars["db_name"],
                user=self.env_vars["db_username"],
                password=self.env_vars["db_password"]
            )
            self.logger.info("Successfully connected to PostgreSQL database")

        self.app = FastAPI(lifespan=startup_event)

        @self.app.post("/v1/query", response_model=QueryResponse)
        def query_vanna(request: QueryRequest):
            try:
                self.logger.info(f"Received query request: {request.question}")

                # Generate SQL
                sql = self.vn.generate_sql(request.question)

                self.logger.info(f"SQL generated: {sql}")

                # Execute SQL and retrieve data
                df = self.vn.run_sql(sql)  # Returns a pandas DataFrame

                self.logger.info(
                    "SQL executed, DataFrame shape: %s",
                    df.shape[0] if df is not None else 0
                )

                sql = str(sql)
                columns = df.columns.tolist()
                rows = df.values.tolist()

                columns = [str(col) for col in columns]
                rows = [list(row) if isinstance(row, tuple)
                        else row for row in rows]

                self.logger.info(
                    "Returning the response with SQL, columns, and rows")

                return QueryResponse(sql=sql,
                                     columns=columns,
                                     rows=rows,
                                     question=request.question)

            except Exception as e:
                self.logger.error(f"Error processing query: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))

    def run(self, host="0.0.0.0", port=8080):
        import uvicorn
        uvicorn.run(self.app, host=host, port=port)


# Request model
class QueryRequest(BaseModel):
    question: str


# Response model
class QueryResponse(BaseModel):
    question: str
    sql: str
    columns: List[str]
    rows: List[List[Any]]


# Expose the app instance
api_instance = PortfolioAnalyzerAPI()
app = api_instance.app  # Expose the app instance for uvicorn

if __name__ == "__main__":
    api_instance.run()
