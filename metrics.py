"""Sales aggregation functions. Each takes the DataFrame from data_loader
and returns a small, chart-ready result — no Streamlit or plotting here."""
import pandas as pd


def total_sales(df: pd.DataFrame) -> float:
    """Sum of all transaction revenue."""
    return float(df["total_amount"].sum())


def total_orders(df: pd.DataFrame) -> int:
    """Count of unique transactions."""
    return int(df["order_id"].nunique())
