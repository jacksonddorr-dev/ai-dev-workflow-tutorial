"""Load and validate the sales CSV described in the PRD's Data Specification."""
import pandas as pd

REQUIRED_COLUMNS = [
    "date", "order_id", "product", "category",
    "region", "quantity", "unit_price", "total_amount",
]


def load_sales_data(csv_path: str) -> pd.DataFrame:
    """Load the sales CSV at csv_path into a validated DataFrame.

    Raises:
        FileNotFoundError: if csv_path does not exist.
        ValueError: if the file is empty or missing required columns.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Sales data file not found: {csv_path}") from None
    except pd.errors.EmptyDataError:
        raise ValueError(f"Sales data file is empty: {csv_path}") from None

    if df.empty:
        raise ValueError(f"Sales data file is empty: {csv_path}")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    return df
