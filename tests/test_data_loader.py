import pandas as pd
import pytest

from data_loader import load_sales_data


def test_load_sales_data_returns_dataframe_with_parsed_dates(tmp_path):
    csv_path = tmp_path / "sales.csv"
    csv_path.write_text(
        "date,order_id,product,category,region,quantity,unit_price,total_amount\n"
        "2024-01-03,ORD-001,Widget,Electronics,North,2,10.00,20.00\n"
    )
    df = load_sales_data(str(csv_path))
    assert len(df) == 1
    assert pd.api.types.is_datetime64_any_dtype(df["date"])
    assert df.loc[0, "total_amount"] == 20.00


def test_load_sales_data_raises_on_missing_file():
    with pytest.raises(FileNotFoundError):
        load_sales_data("does/not/exist.csv")


def test_load_sales_data_raises_on_genuinely_empty_file(tmp_path):
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("")
    with pytest.raises(ValueError, match="empty"):
        load_sales_data(str(csv_path))


def test_load_sales_data_raises_on_missing_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("date,order_id\n2024-01-03,ORD-001\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_sales_data(str(csv_path))


def test_load_sales_data_loads_the_real_dataset():
    df = load_sales_data("data/sales-data.csv")
    assert len(df) == 482
