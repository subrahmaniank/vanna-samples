# Store Analyzer

DVD rental analysis for natural-language questions about movies, customers, rentals, payments, actors, and other DVD store operations. All tables live in the `main` schema.

## Setup

1. Copy `sample.env` to `.env` and set your LLM and Qdrant credentials. The Qdrant collection prefix is `store_analyzer`, separate from other samples.
2. Run `uv run python -m store_analyzer.seed_memory` to load schema and example SQL into Qdrant. This requires FastEmbed to download its local model once.
3. Start the web server with `uv run python -m store_analyzer.store_analyzer_server` on port 8084, or the MCP server with `uv run python -m store_analyzer.store_analyzer_mcp` on port 8087.

## Authentication

Store Analyzer supports user roles:
- **Admin**: Username `admin`, Password `admin#123` (Full SQL inspection and memory management)
- **User**: Username `hillyer`, Password `hillyer` (Natural language query execution)

Access `http://localhost:8084/auth/login` to sign in.

## Entry Points

### Web & API Server (VannaFastAPIServer)

The main server serves both the interactive `<vanna-chat>` web interface and the SSE streaming backend:
- `store_analyzer/store_analyzer_server.py` - Main server (port 8084)
- `store_analyzer/store_analyzer_app.py` - Web application entry point

### MCP Server (Model Context Protocol)

Run the SSE-based MCP server:
- `store_analyzer/store_analyzer_mcp.py` (port 8087)

For API deployment, use:
- `store_analyzer/store_analyzer_api.py` - API entry point (port 8081)

## Database Schema

Key tables in the `main` schema:
- `main.film`: film_id, title, description, release_year, rental_rate, length, rating, special_features
- `main.rental`: rental_id, rental_date, inventory_id, customer_id, return_date, staff_id
- `main.payment`: payment_id, customer_id, staff_id, rental_id, amount, payment_date
- `main.customer`: customer_id, store_id, first_name, last_name, email, address_id, active
- `main.inventory`: inventory_id, film_id, store_id
- `main.actor`: actor_id, first_name, last_name
- `main.film_actor`: actor_id, film_id
- `main.category`: category_id, name
- `main.film_category`: film_id, category_id
- `main.store`: store_id, manager_staff_id, address_id
- `main.staff`: staff_id, first_name, last_name, address_id, email, store_id

## Common Questions

- "Which movies have the highest rental rate?"
- "Show customers who rented more than 5 movies in July 2005"
- "List actors who appeared in action movies"
- "What is the total revenue by store?"

## Legacy Components

- `simple_authorization.py`: Unused Vanna 1.x authorization helper kept for reference. `/auth/login` and `/auth/logout` are implemented inline in `store_analyzer_server.py`; the live agent uses `user_resolver.py` via `StoreAnalyzerUserResolver`.
