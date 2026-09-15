"""Sales aggregation functions. Each takes the DataFrame from data_loader
and returns a small, chart-ready result — no Streamlit or plotting here."""
import pandas as pd


def total_sales(df: pd.DataFrame) -> float:
    """Sum of all transaction revenue."""
    return float(df["total_amount"].sum())


def total_orders(df: pd.DataFrame) -> int:
    """Count of unique transactions."""
    return int(df["order_id"].nunique())


def sales_over_time(df: pd.DataFrame, freq: str = "ME") -> pd.DataFrame:
    """Total sales grouped by time period (monthly by default).

    Returns columns ["period", "total_amount"], sorted chronologically.
    """
    grouped = (
        df.groupby(pd.Grouper(key="date", freq=freq))["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "period"})
    )
    return grouped.sort_values("period").reset_index(drop=True)
