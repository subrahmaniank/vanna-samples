# Vanna Samples

A collection of sample applications demonstrating the use of Vanna AI for natural language to SQL generation and analysis.

## Project Structure

The repository contains three main modules, each demonstrating different use cases of Vanna AI:

### 1. AdventureWorks Module
- **Purpose**: Analyzes the AdventureWorks database
- **Key Components**:
  - `adventureworks_api.py`: FastAPI endpoints for querying the database
  - `adventureworks_app.py`: Web interface for the AdventureWorks demo
  - `adventureworks_mcp.py`: Model Context Protocol implementation
  - Trainers: Contains specialized trainers for DDL, SQL, and documentation

### 2. Portfolio Analyzer Module
- **Purpose**: Analyzes investment portfolios
- **Key Components**:
  - `portfolio_analyzer_api.py`: API endpoints for portfolio analysis
  - `portfolio_analyzer_app.py`: Web interface for portfolio analysis
  - `portfolio_analyzer_mcp.py`: MCP implementation for portfolio analysis
  - Trainers: Specialized trainers for different aspects of portfolio analysis

### 3. Store Analyzer Module
- **Purpose**: Analyzes retail store data
- **Key Components**:
  - `store_analyzer_api.py`: API endpoints for store analysis
  - `store_analyzer_app.py`: Web interface for store analysis
  - `store_analyzer_mcp.py`: MCP implementation for store analysis
  - `simple_authorization.py`: Basic auth implementation
  - Trainers: Specialized trainers for different aspects of store analysis

## Prerequisites

- Python 3.8+
- UV package manager (`pip install uv`)
- PostgreSQL database (for AdventureWorks)
- Required environment variables (see `sample.env` in each module)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd vanna-samples
   ```

2. Install dependencies using UV:
   ```bash
   uv pip install -r requirements.txt
   ```
   
   Or install for production:
   ```bash
   uv pip install --no-deps .
   ```

## Running the Applications

## Service Ports

### Web Applications
Each module runs its web interface on a different port:
- **AdventureWorks Web**: `http://localhost:8086`
- **Portfolio Analyzer Web**: `http://localhost:8085`
- **Store Analyzer Web**: `http://localhost:8084`

### API Servers
Each module runs its API server on a different port:
- **AdventureWorks API**: `http://localhost:8083`
- **Portfolio Analyzer API**: `http://localhost:8082`
- **Store Analyzer API**: `http://localhost:8081`

### MCP Servers
Each MCP server runs on a different port:
- **AdventureWorks MCP**: `http://localhost:8089`
- **Portfolio Analyzer MCP**: `http://localhost:8088`
- **Store Analyzer MCP**: `http://localhost:8087`

### Running the API Server

Each module can be run as a standalone FastAPI application:

```bash
# For AdventureWorks (Port 8083)
uvicorn adventureworks.adventureworks_api:app --host 0.0.0.0 --port 8083 --reload

# For Portfolio Analyzer (Port 8082)
uvicorn portfolio_analyzer.portfolio_analyzer_api:app --host 0.0.0.0 --port 8082 --reload

# For Store Analyzer (Port 8081)
uvicorn store_analyzer.store_analyzer_api:app --host 0.0.0.0 --port 8081 --reload
```

### Running the MCP Server

To run the Model Context Protocol server for any module:

```bash
# For AdventureWorks (Port 8089)
python -m adventureworks.adventureworks_mcp

# For Portfolio Analyzer (Port 8088)
python -m portfolio_analyzer.portfolio_analyzer_mcp

# For Store Analyzer (Port 8087)
python -m store_analyzer.store_analyzer_mcp
```

## Environment Configuration

Each module contains a `sample.env` file with required environment variables. Copy this to `.env` and update the values as needed.

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
