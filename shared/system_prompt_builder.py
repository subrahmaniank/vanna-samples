"""
Enhanced System Prompt Builder for Vanna 2.0.

Extends DefaultSystemPromptBuilder to:
1. Preserve the full official memory workflow (search_saved_correct_tool_uses, save_question_tool_args, save_text_memory).
2. Mandate schema-qualified table references (<schema>.<table>) so cross-schema queries are 100% deterministic.
3. Enforce native UI charting via visualize_data (run_sql -> visualize_data) and strictly prohibit raw Python/matplotlib output.
4. Inject domain-specific schema metadata for AdventureWorks, Store Analyzer, and Portfolio Analyzer.
"""

from typing import Any, List, Optional
try:
    from vanna.core.system_prompt.default import DefaultSystemPromptBuilder
except ImportError:
    class DefaultSystemPromptBuilder:
        def __init__(self, base_prompt: Optional[str] = None):
            self.base_prompt = base_prompt

        async def build_system_prompt(self, user: Any, tools: List[Any]) -> Optional[str]:
            return self.base_prompt or ""


from shared.chart_generator import (
    EnhancedPlotlyChartGenerator,
    EnhancedVisualizeDataArgs,
    EnhancedVisualizeDataTool,
)


class EnhancedSystemPromptBuilder(DefaultSystemPromptBuilder):
    """
    Enhanced system prompt builder that enforces SQL schema qualification,
    native UI visualization tool workflow, and domain schema guidelines.
    """

    def __init__(
        self,
        base_prompt: Optional[str] = None,
        db_guidelines: Optional[str] = None,
        default_schema: Optional[str] = None,
    ):
        super().__init__(base_prompt=base_prompt)
        self.db_guidelines = db_guidelines
        self.default_schema = default_schema

    async def build_system_prompt(
        self,
        user: Any,
        tools: List[Any]
    ) -> Optional[str]:
        # Generate base prompt (including Vanna's memory workflow instructions)
        base = await super().build_system_prompt(user, tools) or ""

        tool_names = [getattr(t, "name", str(t)) for t in tools] if tools else []
        has_visualize = "visualize_data" in tool_names

        extra_sections = []

        # 1. SQL Query and Schema Qualification Rules
        extra_sections.append(
            "\n" + "=" * 60 + "\n"
            "SQL QUERY & SCHEMA QUALIFICATION RULES (MANDATORY):\n"
            "=" * 60 + "\n"
            "- ALWAYS qualify every table name with its exact schema name: `<schema>.<table>`.\n"
            "- Example: use `FROM sales.SalesOrderHeader` instead of `FROM SalesOrderHeader`.\n"
            "- Example: use `JOIN person.Person p ON c.PersonID = p.BusinessEntityID`.\n"
            "- NEVER use unqualified table names like `FROM Customer` or `FROM SalesOrderHeader`.\n"
            "- NEVER guess generic or non-existent table names like `sales`, `orders`, `order`, or `user`.\n"
            "- Always write clean, valid SQL compatible with the target database."
        )

        # 2. Native UI Charting & Visualization Rules
        if has_visualize:
            extra_sections.append(
                "\n" + "=" * 60 + "\n"
                "CHARTING & VISUALIZATION INSTRUCTIONS (MANDATORY):\n"
                "=" * 60 + "\n"
                "- You have access to the `visualize_data` tool for creating interactive charts in the UI.\n"
                "- Supported `chart_type` values: 'bar', 'line', 'pie', 'scatter', 'histogram', 'area', 'table'.\n"
                "- When the user asks for a chart, graph, plot, visual trend, or visualization (e.g. 'bar chart', 'line graph of sales', 'pie chart of categories'):\n"
                "  1. FIRST: Execute the SQL query using `run_sql`.\n"
                "  2. NEXT: Inspect the `run_sql` tool output to get the CSV filename (e.g. `query_results_<id>.csv`).\n"
                "  3. IMMEDIATELY: Call `visualize_data(filename=\"query_results_<id>.csv\", chart_type=\"...\", title=\"...\", x_col=\"...\", y_col=\"...\")` EXACTLY ONCE.\n"
                "     * ALWAYS set `chart_type` to match the user's request (e.g., if user asks for a 'bar chart', set chart_type='bar'; if 'line chart', set chart_type='line'; if 'pie chart', set chart_type='pie').\n"
                "     * If user does not specify a chart type, default to 'bar' for categorical metrics or 'line' for time series.\n"
                "     * Set `x_col` to the dimension/label column (e.g. 'Name', 'Category', 'Territory') and `y_col` to the metric/value column (e.g. 'TotalSales', 'TotalDue', 'Count'). Do NOT use numeric ID columns as axes if a label column exists!\n"
                "  4. CRITICAL STOPPING RULE: Once `visualize_data` has executed, the interactive chart is already rendered in the UI. YOU MUST NOT call `visualize_data` again. YOU MUST NOT execute any more tools. Conclude your turn immediately with a brief textual summary of the observations.\n"
                "  5. NEVER output raw Python code (such as `import matplotlib.pyplot as plt` or `seaborn` scripts).\n"
                "  6. NEVER tell the user to install matplotlib via pip, copy scripts into a notebook, or run code locally.\n"
                "  The UI renders interactive Plotly charts directly in the browser when you call `visualize_data`."
            )



        # 3. Domain Database Schema Reference
        if self.db_guidelines:
            extra_sections.append(
                "\n" + "=" * 60 + "\n"
                "DATABASE SCHEMA REFERENCE:\n"
                "=" * 60 + "\n"
                + self.db_guidelines.strip()
            )

        full_prompt = base + "\n" + "\n".join(extra_sections)
        return full_prompt


# Predefined domain schema guidelines for the sample applications
ADVENTUREWORKS_GUIDELINES = """
AdventureWorks OLTP Database Schemas and Tables:
- Schemas: sales, production, person, humanresources, purchasing.

Key Tables and Relationships (ALWAYS use <schema>.<table>):
1. Orders & Sales:
   - `sales.SalesOrderHeader`: Order headers (SalesOrderID, OrderDate, DueDate, ShipDate, Status, OnlineOrderFlag, CustomerID, SalesPersonID, TerritoryID, SubTotal, TaxAmt, Freight, TotalDue).
   - `sales.SalesOrderDetail`: Order line items (SalesOrderID, SalesOrderDetailID, OrderQty, ProductID, UnitPrice, UnitPriceDiscount, LineTotal).
   - NOTE: There is NO table named `sales` or `orders` or `order`. All order data is in `sales.SalesOrderHeader` and `sales.SalesOrderDetail`.
2. Customers & Stores:
   - `sales.Customer`: (CustomerID, PersonID, StoreID, TerritoryID).
   - `sales.Store`: (BusinessEntityID, Name, SalesPersonID).
   - Customer Names: Join `sales.Customer` with `person.Person` on `sales.Customer.PersonID = person.Person.BusinessEntityID` to get `FirstName`, `LastName`.
3. Sales Territories & Staff:
   - `sales.SalesTerritory`: (TerritoryID, Name, CountryRegionCode, "Group", SalesYTD, SalesLastYear). Note: "Group" is a SQL reserved word, quote it as "Group".
   - `sales.SalesPerson`: (BusinessEntityID, TerritoryID, SalesQuota, Bonus, CommissionPct, SalesYTD, SalesLastYear).
   - `humanresources.Employee`: (BusinessEntityID, NationalIDNumber, LoginID, JobTitle, BirthDate, MaritalStatus, Gender, HireDate).
4. Products & Inventory:
   - `production.Product`: (ProductID, Name, ProductNumber, StandardCost, ListPrice, ProductSubcategoryID).
   - `production.ProductSubcategory`: (ProductSubcategoryID, ProductCategoryID, Name).
   - `production.ProductCategory`: (ProductCategoryID, Name).
5. Purchasing:
   - `purchasing.PurchaseOrderHeader`: (PurchaseOrderID, VendorID, ShipMethodID, OrderDate, TotalDue).
   - `purchasing.PurchaseOrderDetail`: (PurchaseOrderID, ProductID, OrderQty, UnitPrice, LineTotal).
   - `purchasing.Vendor`: (BusinessEntityID, AccountNumber, Name, CreditRating).
"""

STORE_ANALYZER_GUIDELINES = """
DVD Rental Database Schemas and Tables:
- Schema: main (or public for PostgreSQL). ALWAYS use `main.<table>` (or `public.<table>`).

Key Tables:
- `main.film`: (film_id, title, description, release_year, rental_rate, length, rating, special_features)
- `main.rental`: (rental_id, rental_date, inventory_id, customer_id, return_date, staff_id)
- `main.payment`: (payment_id, customer_id, staff_id, rental_id, amount, payment_date)
- `main.customer`: (customer_id, store_id, first_name, last_name, email, address_id, active)
- `main.inventory`: (inventory_id, film_id, store_id)
- `main.actor`: (actor_id, first_name, last_name)
- `main.film_actor`: (actor_id, film_id)
- `main.category`: (category_id, name)
- `main.film_category`: (film_id, category_id)
- `main.store`: (store_id, manager_staff_id, address_id)
- `main.staff`: (staff_id, first_name, last_name, address_id, email, store_id)
"""

PORTFOLIO_ANALYZER_GUIDELINES = """
SEI Portfolio Analyzer Database Schemas and Tables:
- Schema: main. ALWAYS use `main.<table>`.

Key Tables:
- `main.accounts`: (account_id, account_name, account_number, account_type, status, currency)
- `main.positions`: (position_id, account_id, security_id, quantity, cost_basis, market_value, as_of_date)
- `main.transactions`: (transaction_id, account_id, security_id, transaction_type, quantity, price, amount, transaction_date)
- `main.securities`: (security_id, symbol, security_name, asset_class, sector, currency)
- `main.prices`: (security_id, price_date, price)
"""
