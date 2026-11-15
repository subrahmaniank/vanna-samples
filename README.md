# Vanna 2.0 Samples

A collection of sample applications demonstrating the use of **Vanna 2.0** for natural language to SQL generation, agentic retrieval, and interactive database exploration powered by **Snowflake**, **Qdrant Cloud/Service**, and **Azure OpenAI**.

## Architecture (Vanna 2.0)

In version 2.0, Vanna has transitioned to a modular, user-aware Agent framework:
- **`Agent`**: The orchestrator coordinating LLM reasoning, permissions, and tool executions.
- **`SnowflakeRunner`**: Executes queries against Snowflake data warehouses (with PostgreSQL fallback support).
- **`QdrantAgentMemory`**: Cloud/service-connected vector store managing Tool Memory (past SQL examples) and Text Memory (DDL and schema documentation).
- **`UserResolver`**: Context-driven user authentication and Role-Based Access Control (RBAC).
- **`VannaFastAPIServer`**: Serves the modern streaming UI (`<vanna-chat>`) and SSE endpoints.
- **`FastMCP`**: Model Context Protocol servers exposing the agents to AI tools.

---

## Project Structure

The repository contains three modules:

### 1. AdventureWorks Module (`adventureworks/`)
- **Domain**: Order management, purchasing, sales, and inventory
- **Server**: `adventureworks/adventureworks_server.py` (Port `8086`)
- **MCP Server**: `adventureworks/adventureworks_mcp.py` (Port `8089`)
- **Seeder**: `adventureworks/seed_memory.py`

### 2. Store Analyzer Module (`store_analyzer/`)
- **Domain**: DVD rental operations, movies, customers, staff
- **Auth**: RBAC with cookie-based user resolver (`admin` and `hillyer` roles)
- **Server**: `store_analyzer/store_analyzer_server.py` (Port `8084`)
- **MCP Server**: `store_analyzer/store_analyzer_mcp.py` (Port `8087`)
- **Seeder**: `store_analyzer/seed_memory.py`

### 3. Portfolio Analyzer Module (`portfolio_analyzer/`)
- **Domain**: Investment portfolios, assets, transactions, and performance metrics
- **Server**: `portfolio_analyzer/portfolio_analyzer_server.py` (Port `8085`)
- **MCP Server**: `portfolio_analyzer/portfolio_analyzer_mcp.py` (Port `8088`)
- **Seeder**: `portfolio_analyzer/seed_memory.py`

### Shared Components (`shared/`)
- `shared/qdrant_agent_memory.py`: Qdrant Cloud vector memory implementation
- `shared/snowflake_runner.py`: Snowflake SQL runner implementation
- `shared/postgres_runner.py`: PostgreSQL SQL runner implementation
- `shared/env_loader.py`: Unified `.env` loader supporting root and module levels
- `shared/ssl_utils.py`: Enterprise CA bundle & relaxed SSL verification for Python 3.13

---

## Configuration

Copy `sample.env` to `.env` in the project root or inside each module:

```bash
cp sample.env .env
```

Configure the following variables in `.env`:

```env
# Snowflake Database Configuration
SNOWFLAKE_ACCOUNT=your_account.region
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=ADVENTUREWORKS  # or DVDRENTAL, SEI_DEMO
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_ROLE=

# Qdrant Cloud / Managed Service
QDRANT_URL=https://<cluster-id>.<region>.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key

# Azure OpenAI
LLM_ENV=openai
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_MODEL=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

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
```

---

## Running the Servers

### 1. Web & API Servers (VannaFastAPIServer)

Each server serves both the interactive `<vanna-chat>` web interface and the SSE streaming backend:

```bash
# AdventureWorks (Port 8086)
python -m adventureworks.adventureworks_server

# Store Analyzer (Port 8084)
python -m store_analyzer.store_analyzer_server

# Portfolio Analyzer (Port 8085)
python -m portfolio_analyzer.portfolio_analyzer_server
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
