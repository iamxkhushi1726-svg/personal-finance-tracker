import pandas as pd
import io
from typing import Tuple


REQUIRED_COLUMNS = {"date", "description", "category", "amount", "type"}

CATEGORY_COLORS = {
    "Food": "#e74c3c",
    "Transport": "#3498db",
    "Entertainment": "#9b59b6",
    "Utilities": "#e67e22",
    "Education": "#2ecc71",
    "Health": "#1abc9c",
    "Shopping": "#f39c12",
    "Savings": "#34495e",
    "Income": "#27ae60",
    "Other": "#95a5a6",
}

def load_transactions(source) -> Tuple[pd.DataFrame, str]:
    """
    Load transaction CSV from file upload or file path.
    Returns (DataFrame, error_message). error_message is empty on success.
    """
    try:
        if hasattr(source, "read"):
            df = pd.read_csv(io.BytesIO(source.read()))
        else:
            df = pd.read_csv(source)

        missing = REQUIRED_COLUMNS - set(df.columns.str.lower())
        if missing:
            return pd.DataFrame(), f"Missing columns: {missing}"

        df.columns = df.columns.str.lower()
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        df["type"] = df["type"].str.lower().str.strip()
        df["category"] = df["category"].str.strip()
        df = df.sort_values("date").reset_index(drop=True)
        return df, ""

    except Exception as e:
        return pd.DataFrame(), str(e)


def compute_summary(df: pd.DataFrame) -> dict:
    """Compute key financial summary metrics."""
    income_df = df[df["type"] == "income"]
    expense_df = df[df["type"] == "expense"]

    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    net_savings = total_income - total_expense
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0

    top_category = (
        expense_df.groupby("category")["amount"].sum().idxmax()
        if not expense_df.empty else "N/A"
    )
    top_category_amt = (
        expense_df.groupby("category")["amount"].sum().max()
        if not expense_df.empty else 0
    )

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_savings": net_savings,
        "savings_rate": round(savings_rate, 1),
        "top_category": top_category,
        "top_category_amt": top_category_amt,
        "num_transactions": len(df),
        "date_range": f"{df['date'].min().date()} to {df['date'].max().date()}",
    }


def get_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Expense breakdown by category with amount and percentage."""
    expense_df = df[df["type"] == "expense"]
    breakdown = (
        expense_df.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )
    total = breakdown["amount"].sum()
    breakdown["percentage"] = (breakdown["amount"] / total * 100).round(1)
    return breakdown


def get_daily_cashflow(df: pd.DataFrame) -> pd.DataFrame:
    """Daily income vs expense aggregation."""
    daily = (
        df.groupby(["date", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .reset_index()
    )
    if "income" not in daily.columns:
        daily["income"] = 0
    if "expense" not in daily.columns:
        daily["expense"] = 0
    daily["net"] = daily["income"] - daily["expense"]
    return daily