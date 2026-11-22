"""Seed auto finance schema and example SQL into the configured vector store."""

import asyncio
from pathlib import Path

import duckdb

from auto_finance.agent_factory import AUTO_FINANCE_GUIDELINES
from shared.env_loader import EnvironmentLoader
from shared.vector_store_factory import create_agent_memory


EXAMPLES = {
    "How many auto loans were originated each month?": """
        SELECT date_trunc('month', origination_date) AS origination_month,
               count(*) AS loan_count, sum(amount_financed) AS funded_amount
        FROM lending.loans GROUP BY 1 ORDER BY 1
    """,
    "Which dealers originated the most loan volume?": """
        SELECT d.dealer_name, d.region, count(*) AS loan_count,
               sum(l.amount_financed) AS funded_amount
        FROM lending.loans l JOIN lending.dealers d ON l.dealer_id = d.dealer_id
        GROUP BY 1, 2 ORDER BY funded_amount DESC LIMIT 10
    """,
    "What is the current 30 day or greater delinquency rate by credit tier?": """
        WITH latest AS (SELECT max(snapshot_date) AS as_of_date
                        FROM lending.monthly_performance)
        SELECT l.credit_tier, count(*) AS active_loans,
               count(*) FILTER (WHERE p.days_past_due >= 30) AS delinquent_loans,
               round(100.0 * count(*) FILTER (WHERE p.days_past_due >= 30)
                     / nullif(count(*), 0), 2) AS delinquency_rate_pct
        FROM lending.monthly_performance p
        JOIN latest x ON p.snapshot_date = x.as_of_date
        JOIN lending.loans l ON p.loan_id = l.loan_id
        WHERE p.delinquency_bucket <> 'paid_off'
        GROUP BY 1 ORDER BY 1
    """,
    "How does 30 day delinquency vary by origination LTV band?": """
        WITH latest AS (SELECT max(snapshot_date) AS as_of_date
                        FROM lending.monthly_performance)
        SELECT CASE WHEN l.origination_ltv_pct >= 120 THEN '120%+'
                    WHEN l.origination_ltv_pct >= 100 THEN '100-119%'
                    ELSE 'Below 100%' END AS ltv_band,
               count(*) AS active_loans,
               round(100.0 * count(*) FILTER (WHERE p.days_past_due >= 30)
                     / nullif(count(*), 0), 2) AS delinquency_rate_pct
        FROM lending.monthly_performance p
        JOIN latest x ON p.snapshot_date = x.as_of_date
        JOIN lending.loans l ON p.loan_id = l.loan_id
        WHERE p.delinquency_bucket <> 'paid_off'
        GROUP BY 1 ORDER BY 1
    """,
    "Which optional products have outstanding refunds?": """
        SELECT product_type, count(*) AS loan_count,
               sum(refund_due - refund_paid) AS outstanding_refund
        FROM lending.add_on_products
        WHERE refund_due > refund_paid
        GROUP BY 1 ORDER BY outstanding_refund DESC
    """,
}


async def seed_all() -> None:
    config = EnvironmentLoader.load_environment_variables(Path(__file__).parent)
    if config["vector_store"] == "qdrant" and not config["qdrant_url"]:
        raise ValueError("Set QDRANT_URL in auto_finance/.env before seeding Qdrant")
    memory = create_agent_memory(config, collection_prefix="auto_finance")
    if hasattr(memory, "_ensure_collections"):
        try:
            memory.client.get_collections()
        except Exception as exc:
            raise ConnectionError(
                f"Cannot reach Qdrant at {config['qdrant_url']}. For an HTTPS "
                "cluster behind a proxy, try port 443."
            ) from exc
        memory._ensure_collections()
    with duckdb.connect(config["duckdb_path"], read_only=True) as conn:
        ddls = conn.execute("""
            SELECT sql FROM duckdb_tables()
            WHERE schema_name = 'lending' ORDER BY table_name
        """).fetchall()
    for (ddl,) in ddls:
        await memory.save_text_memory(content=ddl, metadata={"type": "ddl"})
    await memory.save_text_memory(
        content=AUTO_FINANCE_GUIDELINES, metadata={"type": "documentation"}
    )
    for question, sql in EXAMPLES.items():
        await memory.save_tool_usage(
            question=question, tool_name="run_sql", args={"sql": sql.strip()},
            success=True, metadata={"seeded": True},
        )
    print(f"Seeded {len(ddls)} table definitions and {len(EXAMPLES)} SQL examples")


if __name__ == "__main__":
    asyncio.run(seed_all())
