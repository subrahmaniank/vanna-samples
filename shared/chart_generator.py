"""
Enhanced Plotly Chart Generator and Visualization Tool for Vanna 2.0.

Provides explicit chart type control ('bar', 'line', 'pie', 'scatter', 'area', 'histogram', 'table'),
smart dimension vs metric column selection (avoiding ID columns for metrics),
and strict completion signals to prevent LLM tool iteration loops.
"""

from typing import Dict, Any, List, Optional, Type, cast
import io
import json
import logging
import pandas as pd
from pydantic import BaseModel, Field

try:
    import plotly.graph_objects as go
    import plotly.express as px
    import plotly.io as pio
    from vanna.integrations.plotly import PlotlyChartGenerator
except ImportError:
    go = None
    px = None
    pio = None
    class PlotlyChartGenerator:
        THEME_COLORS = {"navy": "#023d60", "cream": "#e7e1cf", "teal": "#15a8a8", "orange": "#fe5d26", "magenta": "#bf1363"}
        COLOR_PALETTE = ["#15a8a8", "#fe5d26", "#bf1363", "#023d60"]
        def _apply_standard_layout(self, fig): return fig

try:
    from vanna.core.tool import Tool, ToolContext, ToolResult
    from vanna.components import (
        UiComponent,
        ChartComponent,
        NotificationComponent,
        ComponentType,
        SimpleTextComponent,
    )
    from vanna.capabilities.file_system import FileSystem
    from vanna.integrations.local import LocalFileSystem
except ImportError:
    Tool = object
    ToolContext = Any
    ToolResult = Any
    UiComponent = Any
    ChartComponent = Any
    NotificationComponent = Any
    ComponentType = Any
    SimpleTextComponent = Any
    FileSystem = Any
    LocalFileSystem = Any

logger = logging.getLogger(__name__)


class EnhancedPlotlyChartGenerator(PlotlyChartGenerator):
    """
    Plotly chart generator with explicit chart type dispatch ('bar', 'line', 'pie', etc.)
    and smart column heuristics (e.g. prioritizing named dimensions over numeric ID keys).
    """

    def generate_chart(
        self,
        df: pd.DataFrame,
        title: str = "Chart",
        chart_type: Optional[str] = None,
        x_col: Optional[str] = None,
        y_col: Optional[str] = None,
    ) -> Dict[str, Any]:
        if df.empty:
            raise ValueError("Cannot visualize empty DataFrame")

        # Normalize requested chart type
        requested = (chart_type or "").strip().lower()
        if not requested and title:
            t_lower = title.lower()
            for ct in ["bar", "line", "pie", "scatter", "histogram", "area", "table"]:
                if ct in t_lower:
                    requested = ct
                    break

        all_cols = list(df.columns)
        numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
        date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

        # Separate true metrics from ID/key columns
        metric_candidates = [
            c for c in numeric_cols
            if not c.lower().endswith("id") and not c.lower().endswith("code") and not c.lower().endswith("key")
        ]
        dim_candidates = [
            c for c in cat_cols
            if not c.lower().endswith("id") and not c.lower().endswith("code")
        ]

        # Determine best X (dimension) and Y (metric)
        if x_col and x_col in all_cols:
            actual_x = x_col
        elif date_cols and (requested == "line" or requested == "area"):
            actual_x = date_cols[0]
        elif dim_candidates:
            actual_x = dim_candidates[0]
        elif cat_cols:
            actual_x = cat_cols[0]
        elif all_cols:
            actual_x = all_cols[0]
        else:
            actual_x = None

        if y_col and y_col in all_cols:
            actual_y = y_col
        elif metric_candidates:
            actual_y = metric_candidates[0]
        elif numeric_cols:
            actual_y = numeric_cols[0]
        elif len(all_cols) > 1 and all_cols[1] != actual_x:
            actual_y = all_cols[1]
        else:
            actual_y = None

        # Dispatch based on requested chart type
        fig: Optional[Any] = None

        if requested == "bar":
            fig = px.bar(
                df,
                x=actual_x,
                y=actual_y,
                title=title,
                color_discrete_sequence=[self.THEME_COLORS["teal"], self.THEME_COLORS["orange"]],
            )
        elif requested == "line":
            fig = px.line(
                df,
                x=actual_x,
                y=actual_y,
                title=title,
                markers=True,
                color_discrete_sequence=[self.THEME_COLORS["teal"]],
            )
        elif requested == "pie":
            fig = px.pie(
                df,
                names=actual_x,
                values=actual_y,
                title=title,
                color_discrete_sequence=self.COLOR_PALETTE,
            )
        elif requested == "scatter":
            fig = px.scatter(
                df,
                x=actual_x,
                y=actual_y,
                title=title,
                color_discrete_sequence=[self.THEME_COLORS["magenta"]],
            )
        elif requested == "area":
            fig = px.area(
                df,
                x=actual_x,
                y=actual_y,
                title=title,
                color_discrete_sequence=[self.THEME_COLORS["teal"]],
            )
        elif requested == "histogram":
            fig = px.histogram(
                df,
                x=actual_y or actual_x,
                title=title,
                color_discrete_sequence=[self.THEME_COLORS["teal"]],
            )
        elif requested == "table":
            fig = self._create_table(df, title)

        if fig is not None:
            self._apply_standard_layout(fig)
            return json.loads(pio.to_json(fig))

        # Default smart fallback:
        # If there is at least one categorical dimension and one metric, default to BAR chart
        if (cat_cols or dim_candidates) and (metric_candidates or numeric_cols):
            fig = px.bar(
                df,
                x=actual_x,
                y=actual_y,
                title=title,
                color_discrete_sequence=[self.THEME_COLORS["teal"], self.THEME_COLORS["orange"]],
            )
            self._apply_standard_layout(fig)
            return json.loads(pio.to_json(fig))

        # Delegate to base heuristics
        return super().generate_chart(df, title)


class EnhancedVisualizeDataArgs(BaseModel):
    """Arguments for EnhancedVisualizeDataTool."""

    filename: str = Field(description="Name of the CSV file to visualize")
    title: Optional[str] = Field(
        default=None, description="Optional title for the chart"
    )
    chart_type: Optional[str] = Field(
        default=None,
        description="Chart type: 'bar', 'line', 'pie', 'scatter', 'histogram', 'area', or 'table'. Defaults to automatic selection."
    )
    x_col: Optional[str] = Field(
        default=None,
        description="Optional column name for X-axis (dimension/category/date)."
    )
    y_col: Optional[str] = Field(
        default=None,
        description="Optional column name for Y-axis (metric/numeric value)."
    )


class EnhancedVisualizeDataTool(Tool[EnhancedVisualizeDataArgs]):
    """
    Enhanced visualization tool supporting explicit chart types ('bar', 'line', 'pie', etc.),
    custom X/Y column mappings, and clear completion instructions to prevent LLM iteration loops.
    """

    def __init__(
        self,
        file_system: Optional[FileSystem] = None,
        plotly_generator: Optional[PlotlyChartGenerator] = None,
    ):
        self.file_system = file_system or LocalFileSystem()
        self.plotly_generator = plotly_generator or EnhancedPlotlyChartGenerator()

    @property
    def name(self) -> str:
        return "visualize_data"

    @property
    def description(self) -> str:
        return (
            "Create an interactive visualization from a CSV file. "
            "Supports chart_type ('bar', 'line', 'pie', 'scatter', 'histogram', 'area', 'table')."
        )

    def get_args_schema(self) -> Type[EnhancedVisualizeDataArgs]:
        return EnhancedVisualizeDataArgs

    async def execute(
        self, context: ToolContext, args: EnhancedVisualizeDataArgs
    ) -> ToolResult:
        try:
            logger.info(f"Starting visualization for file: {args.filename} (type: {args.chart_type})")

            csv_content = await self.file_system.read_file(args.filename, context)
            df = pd.read_csv(io.StringIO(csv_content))
            title = args.title or f"Visualization of {args.filename}"

            chart_type_val = (args.chart_type or "").strip().lower() or None
            chart_dict = self.plotly_generator.generate_chart(
                df,
                title=title,
                chart_type=chart_type_val,
                x_col=args.x_col,
                y_col=args.y_col
            )

            resolved_chart_type = chart_type_val or "bar"
            row_count = len(df)
            col_count = len(df.columns)

            chart_component = ChartComponent(
                chart_type=resolved_chart_type,
                data=chart_dict,
                title=title,
                config={
                    "data_shape": {"rows": row_count, "columns": col_count},
                    "source_file": args.filename,
                    "chart_type": resolved_chart_type,
                },
            )

            result_msg = (
                f"Interactive {resolved_chart_type} chart successfully generated and rendered in the UI from '{args.filename}'. "
                "The visualization is now visible to the user. "
                "DO NOT call visualize_data again. Do not execute any further tools. "
                "Now summarize the chart data and key insights for the user to conclude your response."
            )

            return ToolResult(
                success=True,
                result_for_llm=result_msg,
                ui_component=UiComponent(
                    rich_component=chart_component,
                    simple_component=SimpleTextComponent(text=result_msg),
                ),
                metadata={
                    "filename": args.filename,
                    "rows": row_count,
                    "columns": col_count,
                    "chart_type": resolved_chart_type,
                    "chart": chart_dict,
                },
            )

        except Exception as e:
            logger.error(f"Error creating visualization for {args.filename}: {e}", exc_info=True)
            error_message = f"Error creating visualization: {str(e)}"
            return ToolResult(
                success=False,
                result_for_llm=error_message,
                ui_component=UiComponent(
                    rich_component=NotificationComponent(
                        type=ComponentType.NOTIFICATION,
                        level="error",
                        message=error_message,
                    ),
                    simple_component=SimpleTextComponent(text=error_message),
                ),
                error=str(e),
                metadata={"error_type": "visualization_error"},
            )
