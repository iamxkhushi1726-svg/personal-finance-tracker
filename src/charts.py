import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.processor import CATEGORY_COLORS

THEME = "plotly_dark"


def pie_chart_expenses(breakdown: pd.DataFrame):
    """Donut chart of expense breakdown by category."""
    colors = [CATEGORY_COLORS.get(c, "#95a5a6") for c in breakdown["category"]]
    fig = px.pie(
        breakdown,
        values="amount",
        names="category",
        title="Expense Breakdown by Category",
        hole=0.45,
        color_discrete_sequence=colors,
        template=THEME,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title_font_size=15, margin=dict(t=50, b=20))
    return fig


def bar_chart_categories(breakdown: pd.DataFrame):
    """Horizontal bar chart of spending by category."""
    breakdown = breakdown.sort_values("amount")
    colors = [CATEGORY_COLORS.get(c, "#95a5a6") for c in breakdown["category"]]
    fig = go.Figure(go.Bar(
        x=breakdown["amount"],
        y=breakdown["category"],
        orientation="h",
        marker_color=colors,
        text=[f"₹{v:,.0f}" for v in breakdown["amount"]],
        textposition="outside",
    ))
    fig.update_layout(
        title="Spending by Category",
        template=THEME,
        title_font_size=15,
        margin=dict(t=50, b=20, r=80),
        xaxis_title="Amount (₹)",
    )
    return fig


def line_chart_cashflow(daily: pd.DataFrame):
    """Line chart of daily income vs expenses."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["income"],
        name="Income", line=dict(color="#2ecc71", width=2),
        fill="tozeroy", fillcolor="rgba(46,204,113,0.1)",
    ))
    fig.add_trace(go.Scatter(
        x=daily["date"], y=daily["expense"],
        name="Expense", line=dict(color="#e74c3c", width=2),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.1)",
    ))
    fig.update_layout(
        title="Daily Cash Flow — Income vs Expenses",
        template=THEME,
        hovermode="x unified",
        title_font_size=15,
        margin=dict(t=50, b=20),
    )
    return fig


def waterfall_chart(summary: dict):
    """Waterfall chart showing income → expenses → savings."""
    fig = go.Figure(go.Waterfall(
        name="Finance",
        orientation="v",
        measure=["absolute", "relative", "total"],
        x=["Total Income", "Total Expenses", "Net Savings"],
        y=[
            summary["total_income"],
            -summary["total_expense"],
            None,
        ],
        connector=dict(line=dict(color="rgba(255,255,255,0.3)")),
        decreasing=dict(marker_color="#e74c3c"),
        increasing=dict(marker_color="#2ecc71"),
        totals=dict(marker_color="#3498db"),
        text=[
            f"₹{summary['total_income']:,.0f}",
            f"₹{summary['total_expense']:,.0f}",
            f"₹{summary['net_savings']:,.0f}",
        ],
        textposition="outside",
    ))
    fig.update_layout(
        title="Financial Waterfall",
        template=THEME,
        title_font_size=15,
        margin=dict(t=50, b=20),
    )
    return fig