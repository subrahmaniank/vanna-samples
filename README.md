# Vanna 2.0 Samples

A collection of sample applications demonstrating the use of **Vanna 2.0** for natural language to SQL generation, agentic retrieval, and interactive database exploration powered by **Snowflake**, **Qdrant Cloud/Service**, and **Azure OpenAI**.

## Architecture (Vanna 2.0)

In version 2.0, Vanna has transitioned to a modular, user-aware Agent framework:
- **`Agent`**: The orchestrator coordinating LLM reasoning, permissions, and tool executions.
- **`SqlRunner` / `DatabaseFactory`**: Dynamic database switching between **DuckDB**, **Snowflake**, and **PostgreSQL** via configuration.
- **`DuckDbRunner`**: High-performance embedded analytics runner for local files (`.duckdb`), in-memory (`:memory:`), or MotherDuck.
- **`SnowflakeRunner`**: Cloud data warehouse runner utilizing `snowflake-connector-python[pandas]`.
- **`PostgresRunner`**: PostgreSQL runner utilizing `psycopg2`.
- **`AgentMemory` / `VectorStoreFactory`**: Dynamic vector store switching between **Qdrant Cloud**, **ChromaDB**, and **FAISS** via configuration.
- **`QdrantAgentMemory`**: Cloud/service-connected vector store managing Tool Memory (past SQL examples) and Text Memory (DDL and schema documentation).
- **`ChromaAgentMemory`**: Persistent local disk storage backed by ChromaDB.
- **`FaissAgentMemory`**: High-performance in-memory and file-backed vector similarity search backed by FAISS.
- **`UserResolver`**: Context-driven user authentication and Role-Based Access Control (RBAC).
- **`VannaFastAPIServer`**: Serves the modern streaming UI (`<vanna-chat>`) and SSE endpoints.
- **`FastMCP`**: Model Context Protocol servers exposing the agents to AI tools.

---

## Project Structure

The repository contains four modules:

### 1. AdventureWorks Module (`adventureworks/`)
- **Domain**: Order management, purchasing, sales, and inventory
- **Server**: `adventureworks/adventureworks_server.py` (Port `8086`)
- **MCP Server**: `adventureworks/adventureworks_mcp.py` (Port `8089`)
- **Entry Points**: `adventureworks/adventureworks_app.py`, `adventureworks/adventureworks_api.py` (port 8083)
- **Seeder**: `adventureworks/seed_memory.py`

### 2. Store Analyzer Module (`store_analyzer/`)
- **Domain**: DVD rental operations, movies, customers, staff
- **Auth**: RBAC with cookie-based user resolver (`admin` and `hillyer` roles)
- **Server**: `store_analyzer/store_analyzer_server.py` (Port `8084`)
- **MCP Server**: `store_analyzer/store_analyzer_mcp.py` (Port `8087`)
- **Entry Points**: `store_analyzer/store_analyzer_app.py`, `store_analyzer/store_analyzer_api.py` (port 8081)
- **Seeder**: `store_analyzer/seed_memory.py`

### 3. Portfolio Analyzer Module (`portfolio_analyzer/`)
- **Domain**: Investment portfolios, assets, transactions, and performance metrics
- **Server**: `portfolio_analyzer/portfolio_analyzer_server.py` (Port `8085`)
- **MCP Server**: `portfolio_analyzer/portfolio_analyzer_mcp.py` (Port `8088`)
- **Entry Points**: `portfolio_analyzer/portfolio_analyzer_app.py`, `portfolio_analyzer/portfolio_analyzer_api.py` (port 8082)
- **Seeder**: `portfolio_analyzer/seed_memory.py`

### 4. Auto Finance Module (`auto_finance/`)
- **Domain**: Synthetic auto loan originations, delinquency, payments, collections, and refunds
- **Server**: `auto_finance/auto_finance_server.py` (Port `8090`)
- **MCP Server**: `auto_finance/auto_finance_mcp.py` (Port `8091`)
- **Tools**: `auto_finance/sql_tool.py` (custom SQL tool with CTE support)
- **Seeder**: `auto_finance/seed_memory.py`
- **Database**: `auto_finance/auto_finance.duckdb`, built in the sibling `duckdb-setup` repository

### Shared Components (`shared/`)
- `shared/database_factory.py`: Central runner factory switching between DuckDB, Snowflake, and Postgres
- `shared/duckdb_runner.py`: DuckDB SQL runner implementation
- `shared/snowflake_runner.py`: Snowflake SQL runner implementation
- `shared/postgres_runner.py`: PostgreSQL SQL runner implementation
- `shared/qdrant_agent_memory.py`: Qdrant Cloud vector memory implementation
- `shared/faiss_agent_memory.py`: FAISS high-performance vector memory implementation
- `shared/chroma_agent_memory.py`: ChromaDB persistent memory implementation
- `shared/env_loader.py`: Unified `.env` loader supporting root and module levels
- `shared/ssl_utils.py`: System certificate trust for outbound HTTPS
- `shared/memory_seeder.py`: Bridge for legacy `vn.train()` calls into Vanna 2.0 QdrantAgentMemory
- `shared/llm_factory.py`: LLM service factory supporting OpenRouter, Bedrock Mantle, Azure OpenAI, and OpenAI
- `shared/system_prompt_builder.py`: Enhanced system prompt builder with schema qualification and native UI charting
- `shared/chart_generator.py`: Enhanced Plotly chart generator for native UI visualizations

---

## Configuration

Copy `sample.env` to `.env` in the project root or inside each module:

```bash
cp sample.env .env
```

Configure the following variables in `.env`:

```env
# -------------------------------------------------------------
# Active Database Selector: 'duckdb' | 'snowflake' | 'postgres'
# -------------------------------------------------------------
DATABASE_TYPE=duckdb
DUCKDB_PATH=adventureworks.duckdb

# -------------------------------------------------------------
# Active Vector Store Selector: 'qdrant' | 'chromadb' | 'faiss'
# -------------------------------------------------------------
VECTOR_STORE=qdrant
VANNA_MAX_TOOL_ITERATIONS=25
QDRANT_URL=https://<cluster-id>.<region>.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key

# -------------------------------------------------------------
# Active LLM Provider Selector: 'bedrock_mantle' | 'azure_openai' | 'openai'
# -------------------------------------------------------------
LLM_PROVIDER=bedrock_mantle

# 1. AWS Bedrock Mantle (Native OpenAI-compatible endpoint)
BEDROCK_MANTLE_ENDPOINT=https://bedrock-mantle.us-east-1.api.aws/v1
BEDROCK_MANTLE_API_KEY=your_bedrock_api_key
BEDROCK_MANTLE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
AWS_REGION=us-east-1

# 2. Azure OpenAI (alternative)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_MODEL=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

`VANNA_MAX_TOOL_ITERATIONS` sets the maximum number of tool executions per chat response. The default is 25; increase it in the module's `.env` if a task still reaches the limit, then restart the server.

---

## Seeding Memory (DDL, Docs, and SQL)

Populate your Qdrant vector store with schema DDL, documentation, and known-good queries:

```bash
# Seed AdventureWorks
python -m adventureworks.seed_memory

# Seed Store Analyzer
python -m store_analyzer.seed_memory

# Seed Portfolio Analyzer
python -m portfolio_analyzer.seed_memory

# Seed Auto Finance
python -m auto_finance.seed_memory
```

---

## Running the Servers

### Corporate proxy certificates

The servers use `truststore` to verify HTTPS certificates against the operating system trust store. On Windows, install your organization's Zscaler **root CA certificate** in **Trusted Root Certification Authorities** (Current User or Local Machine). If your organization provides an intermediate CA certificate, install it in **Intermediate Certification Authorities**. Use your organization's approved certificate installation process.

Install the project dependencies with `uv sync`, then restart the server. The same system trust applies to the Hugging Face model download, the LLM endpoint, and remote Qdrant HTTPS requests. If `SSL_CERT_FILE` or `REQUESTS_CA_BUNDLE` is set to a bundle without the Zscaler CA, remove those overrides before launching the server.

The first Qdrant query still downloads the FastEmbed model to the local machine; Qdrant being remote does not remove that download. The `datetime.utcnow()` warnings in the logs are unrelated to the TLS error.

### 1. Web & API Servers (VannaFastAPIServer)

Each server serves both the interactive `<vanna-chat>` web interface and the SSE streaming backend:

```bash
# AdventureWorks (Port 8086)
python -m adventureworks.adventureworks_server

# Store Analyzer (Port 8084)
python -m store_analyzer.store_analyzer_server

# Portfolio Analyzer (Port 8085)
python -m portfolio_analyzer.portfolio_analyzer_server

# Auto Finance (Port 8090)
python -m auto_finance.auto_finance_server
```

Or using uvicorn directly:
```bash
uvicorn adventureworks.adventureworks_server:app --host 0.0.0.0 --port 8086 --reload
```

### 2. MCP Servers (Model Context Protocol)

Run the SSE-based MCP servers:

```bash
# AdventureWorks MCP (Port 8089)
python -m adventureworks.adventureworks_mcp

# Store Analyzer MCP (Port 8087)
python -m store_analyzer.store_analyzer_mcp

# Portfolio Analyzer MCP (Port 8088)
python -m portfolio_analyzer.portfolio_analyzer_mcp

# Auto Finance MCP (Port 8091)
python -m auto_finance.auto_finance_mcp
```

---

## Authentication in Store Analyzer

Store Analyzer supports user roles:
- **Admin**: Username `admin`, Password `admin#123` (Full SQL inspection and memory management)
- **User**: Username `hillyer`, Password `hillyer` (Natural language query execution)

Access `http://localhost:8084/auth/login` to sign in.

---

## License

This project is licensed under the MIT License.
