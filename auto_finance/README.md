# Auto Finance Analysis

Synthetic DuckDB portfolio for natural-language questions about auto loan originations,
dealer performance, delinquency, payments, collections, and optional product refunds.
All tables live in the `lending` schema. No customer personal data is included.

## Customer demo story

Start with a broad question, then drill into the loans behind the answer:
**Where is the portfolio growing, where is repayment risk emerging, and what
should the team investigate?** Origination, negative equity, delinquency, and
servicing are useful themes for an auto finance customer. They also appear in
[Federal Reserve research on auto loan delinquency](https://www.federalreserve.gov/econres/notes/feds-notes/a-note-on-recent-dynamics-of-consumer-delinquency-rates-20251124.html)
and [CFPB research on financed negative equity](https://www.consumerfinance.gov/data-research/research-reports/data-spotlight-negative-equity-findings-from-the-auto-finance-data-pilot/).
Those publications informed the demo themes; their data was **not** used to
generate this database.

| Business data | Implemented in this database | Questions Vanna can answer |
| --- | --- | --- |
| Applications and loan contracts | `lending.applications` has application date, decision, dealer, credit tier, vehicle value, down payment, and trade-in negative equity. Approved applications become `lending.loans`, with origination date, amount financed, APR, term, monthly payment, and origination LTV. | “How have approval rates and loan terms changed?” “Which dealers originated the most loans in 2025?” |
| Vehicles and trade-ins | Vehicle type (`new` or `used`), value, down payment, negative equity, and LTV are on applications and loans. | “Which origination months have the highest share of loans above 120% LTV?” |
| Monthly loan snapshots | `lending.monthly_performance` has month end, balance, days past due, delinquency bucket, and a `paid_off` status. | “Which origination cohorts have the highest 30+ day delinquency rate at month six?” “Where did delinquency rise from September to October 2026?” |
| Payments | `lending.payments` has one installment row per loan-month with due date, amount due, payment date, and amount paid. | “What share of September 2026 installments were unpaid?” “How many loans moved from 30+ days past due in September to current in October?” |
| Collections | `lending.collections` has contact date, channel, and outcome for 30+ day delinquent loan-months. | “What share of contacted accounts were current in the next monthly snapshot?” |
| Optional products and refunds | `lending.add_on_products` has product type, cancellation date, refund due, and refund paid. | “Which loans have an outstanding optional-product refund?” |

### Source and limits of the synthetic data

The source is the SQL in `duckdb-setup/auto_finance/build.py` in the sibling
repository. It generates the records directly with DuckDB `range()`, fixed
dates, arithmetic based on IDs, and `hash(loan_id, month_index)` for delinquency
patterns. It does not download files, sample a real lender's portfolio, or use
the linked Federal Reserve and CFPB datasets. Dealer names are invented labels;
there are no borrower names or personal identifiers. Rebuilding with the same
script and DuckDB version produces the same demo data.

The current build has **30,000 applications, 24,000 loans, 60 dealers, and
470,379 monthly snapshots**. Snapshots cover month ends from January 2024
through October 2026, with each loan appearing only after origination. This
differs from the original proposal of roughly 50,000 loans with 24 months of
linked history. Balances and payments use simplified formulas, and delinquency
is generated from rules rather than observed repayment behavior. The data is
suited to demonstrating joins, cohort comparisons, and charts; it is not a
credit-risk model or a realistic forecast.

The initial proposal also included vehicle make/model, trade-in payoff
balances, payment reversals, payment arrangements, and explicit payoff dates.
Those fields are **not present**. The current data has a `paid_off` snapshot
status, but does not model the full payoff and refund process. Avoid questions
that require those missing fields. Dealer funding totals are also quite
similar, so a “fastest-growing dealers” ranking is less compelling than the
LTV and delinquency examples below.

### Suggested live walkthrough

1. **Growth:** “Show monthly loan originations in 2025, then break a month down by dealer.”
2. **Risk:** “Which origination cohorts have the highest 30+ day delinquency rate at six months on book?”
3. **Drill-down:** “For that cohort, compare the rate by dealer, new versus used vehicle, and LTV band.”
4. **Operations:** “Of loans 30+ days past due in September 2026, how many were current in October 2026?”
5. **Exception:** “Which loans have a positive outstanding optional-product refund?”

This sequence moves from a portfolio trend to loan-level records that a team
can review. Comparisons such as collections contact versus later cure are
observed associations, not evidence that the contact caused the cure.

## Setup

1. Generate `auto_finance.duckdb` in the sibling `duckdb-setup/auto_finance` folder
   with `uv run python auto_finance/build.py` from that repository.
2. Copy the database into this folder (already done for the initial setup).
3. Copy `sample.env` to `.env` and set your LLM and Qdrant credentials. The
   Qdrant collection prefix is `auto_finance`, separate from other samples.
4. Run `uv run python -m auto_finance.seed_memory` to load schema and example
   SQL into Qdrant. This requires FastEmbed to download its local model once.

## Entry Points

### Web & API Server (VannaFastAPIServer)

The main server serves both the interactive `<vanna-chat>` web interface and the SSE streaming backend:
- `auto_finance/auto_finance_server.py` - Main server (port 8090)

### MCP Server (Model Context Protocol)

Run the SSE-based MCP server:
- `auto_finance/auto_finance_mcp.py` - MCP server (port 8091)

The `auto_finance/sql_tool.py` file provides enhanced SQL execution tools:
- `AutoFinanceRunSqlTool`: Extends Vanna's RunSqlTool to handle CTEs (WITH queries) by automatically wrapping them in subqueries for CSV export. Vanna's RunSqlTool writes a CSV only when the statement starts with SELECT; a read-only CTE returning rows needs the same path.
- `AutoFinanceVisualizeDataTool`: Customizes filename handling to prevent inventing filenames. Uses only the exact CSV filename returned by a successful run_sql call in the current conversation.

## Chart demo questions

Ask these as separate questions in the web chat. Each prompt names the chart
type and axes so Vanna can pass them to `visualize_data`. The expected row
counts below were checked against the included database.

| Chart | Ask Vanna | Expected result |
| --- | --- | --- |
| Line | **Show a line chart of the number of loans originated in each month of 2025.** Use month on the X-axis and loan count on the Y-axis, with one row per month in date order. | 12 monthly points with varying heights. |
| Bar | **Show a bar chart of originated loan counts in four LTV bands: below 80%, 80-99%, 100-119%, and 120% or more.** Use LTV band on the X-axis and loan count on the Y-axis. | 4 bars with visibly different counts. |
| Pie | **Show a pie chart of loan counts by delinquency bucket on 2026-10-31, including paid-off loans.** Use `delinquency_bucket` for slice labels and loan count for slice size. | 5 slices: current, 1-29, 30-59, 60+, and paid off. |
| Area | **Show an area chart of cumulative funded loan amount by month during 2025.** Use month on the X-axis and running total of `amount_financed` on the Y-axis, with one row per month. | 12 monthly points with an increasing total. |
| Scatter | **Show a scatter chart of vehicle value versus amount financed for the first 300 loans originated in 2025, ordered by loan ID.** Use `vehicle_value` on the X-axis and `amount_financed` on the Y-axis; keep one point per loan. | 300 loan-level points. |
| Histogram | **Show a histogram of origination LTV percentage for the first 3,000 loans ordered by loan ID.** Use the raw `origination_ltv_pct` values, one row per loan, rather than pre-grouped bands. | 3,000 values distributed across LTV ranges. |
| Table | **Show a table of the first 15 loans by loan ID with a positive outstanding optional-product refund.** Include loan ID, product type, refund due, refund paid, and the difference. | 15 loan-level rows. |

For a shorter business demo, start with the line, bar, pie, and scatter
questions. The earlier credit-tier and product-type questions produced two rows
because those fields have two categories in this synthetic dataset.

The data is synthetic. The observed differences support exploration and demo
questions; they do not establish causal effects or predict future defaults.
