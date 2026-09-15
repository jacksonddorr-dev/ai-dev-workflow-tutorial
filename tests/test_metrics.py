import pandas as pd

from metrics import total_sales, total_orders


def _sample_df():
    return pd.DataFrame({
        "order_id": ["ORD-1", "ORD-2", "ORD-3"],
        "total_amount": [100.0, 50.5, 25.25],
    })


def test_total_sales_sums_all_transactions():
    assert total_sales(_sample_df()) == 175.75


def test_total_orders_counts_unique_order_ids():
    assert total_orders(_sample_df()) == 3


def test_total_orders_does_not_double_count_repeated_order_id():
    df = pd.DataFrame({
        "order_id": ["ORD-1", "ORD-1"],
        "total_amount": [10.0, 5.0],
    })
    assert total_orders(df) == 1
