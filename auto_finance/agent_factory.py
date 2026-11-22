"""Vanna agent for the synthetic auto finance portfolio."""

from pathlib import Path

from shared.database_factory import create_sql_runner
from shared.env_loader import EnvironmentLoader
from shared.llm_factory import create_llm_service
from shared.system_prompt_builder import EnhancedSystemPromptBuilder
from shared.vector_store_factory import create_agent_memory
from auto_finance.user_resolver import AutoFinanceUserResolver
from auto_finance.sql_tool import AutoFinanceRunSqlTool, AutoFinanceVisualizeDataTool

from vanna import Agent, AgentConfig
from vanna.core.agent.config import UiFeatures
from vanna.core.registry import ToolRegistry
from vanna.integrations.local import LocalFileSystem
from vanna.tools.agent_memory import (
    SearchSavedCorrectToolUsesTool,
    SaveQuestionToolArgsTool,
    SaveTextMemoryTool,
)


AUTO_FINANCE_GUIDELINES = """
Synthetic auto finance portfolio, as of 2026-10-31. All tables are in the lending schema.
Use exact schema-qualified names and read-only SELECT queries.
- lending.dealers: dealer_id, dealer_name, region. One row per dealer.
- lending.applications: application_id, application_date, dealer_id, decision
  ('approved' or 'declined'), credit_tier ('prime' or 'nonprime'), vehicle_type,
  vehicle_value, down_payment, trade_in_negative_equity. One row per application.
- lending.loans: loan_id (= approved application_id), application_id, dealer_id,
  origination_date, credit_tier, vehicle_type, vehicle_value, down_payment,
  trade_in_negative_equity, amount_financed, apr_pct, term_months,
  monthly_payment, origination_ltv_pct. One row per originated loan.
- lending.monthly_performance: loan_id, snapshot_date, months_on_book,
  delinquency_bucket ('current', '1_29', '30_59', '60_plus', 'paid_off'),
  days_past_due, outstanding_balance. One row per loan per month. For current
  portfolio metrics, use MAX(snapshot_date), then exclude 'paid_off' as needed.
  30+ delinquency means days_past_due >= 30. Compute a rate as delinquent
  loan count / active loan count in the SAME snapshot and group.
- lending.payments: loan_id, installment_month, due_date, payment_date,
  amount_due, amount_paid. One row per loan per month; payment_date is NULL
  when unpaid. Join by loan_id AND snapshot_date = installment_month when
  comparing payment and performance records.
- lending.collections: loan_id, contact_date, channel, outcome. One row for
  each 30+ delinquent loan-month; join on loan_id and snapshot_date=contact_date.
- lending.add_on_products: loan_id, product_type, price, cancellation_date,
  refund_due, refund_paid. One row per loan with an optional product.
  Outstanding refund = refund_due - refund_paid when positive.
Join loans to dealers on dealer_id, applications to loans on application_id,
and child tables to loans on loan_id. For vintage analysis, group by the
origination month and compare cohorts at the same months_on_book.
These are synthetic observations; do not claim a segment or collection contact
caused an outcome or present this dataset as real customer data.
"""


def create_agent():
    config = EnvironmentLoader.load_environment_variables(
        module_path=Path(__file__).parent, default_db_name="AUTO_FINANCE"
    )
    db_path = Path(config["duckdb_path"])
    if config["database_type"] == "duckdb" and not db_path.is_file():
        raise FileNotFoundError(
            f"Auto finance database not found: {db_path}. Copy the generated file "
            "from duckdb-setup/auto_finance."
        )

    sql_runner = create_sql_runner(config, default_db_name="AUTO_FINANCE")
    agent_memory = create_agent_memory(config, collection_prefix="auto_finance")
    llm_service = create_llm_service(config)
    output_dir = Path(__file__).parent / ".vanna_fs"
    output_dir.mkdir(exist_ok=True)
    file_system = LocalFileSystem(working_directory=output_dir)

    tools = ToolRegistry()
    tools.register_local_tool(
        AutoFinanceRunSqlTool(sql_runner=sql_runner, file_system=file_system),
        access_groups=["user", "admin"],
    )
    tools.register_local_tool(
        AutoFinanceVisualizeDataTool(file_system=file_system),
        access_groups=["user", "admin"],
    )
    tools.register_local_tool(SearchSavedCorrectToolUsesTool(), access_groups=["user", "admin"])
    tools.register_local_tool(SaveQuestionToolArgsTool(), access_groups=["user", "admin"])
    tools.register_local_tool(SaveTextMemoryTool(), access_groups=["user", "admin"])

    return Agent(
        llm_service=llm_service,
        tool_registry=tools,
        agent_memory=agent_memory,
        user_resolver=AutoFinanceUserResolver(),
        config=AgentConfig(
            max_tool_iterations=config["max_tool_iterations"],
            stream_responses=True,
            ui_features=UiFeatures(feature_group_access={
                "tool_names": ["admin"], "tool_arguments": ["admin"],
                "tool_error": ["admin"], "tool_invocation_message_in_chat": [],
            }),
        ),
        system_prompt_builder=EnhancedSystemPromptBuilder(db_guidelines=AUTO_FINANCE_GUIDELINES),
    )
