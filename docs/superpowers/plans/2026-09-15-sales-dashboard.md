# ShopSmart Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 ShopSmart sales dashboard — KPI cards, a sales trend line chart, and category/region bar charts — from `data/sales-data.csv`, ready to deploy to Streamlit Community Cloud.

**Architecture:** A single-page Streamlit app (`app.py`) renders the UI. Three small, pure-function modules do the work behind it: `data_loader.py` (load + validate the CSV), `metrics.py` (aggregations: totals, trend, category/region breakdowns), and `formatting.py` (currency/number display strings). Keeping the data logic out of `app.py` and free of Streamlit calls is what makes it unit-testable — `app.py` itself stays a thin rendering layer that's verified by running it, not by pytest.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly (Express), pytest.

**Spec:** `prd/ecommerce-analytics.md` — this plan's tasks are labeled with the milestone IDs from `TASKS.md` (`TASK-1`…`TASK-7`), which already breaks the PRD's M1–M7 into acceptance criteria. This plan's own task numbers (Task 1, Task 2, …) are a separate sequence — don't conflate a plan "Task 3" with milestone `TASK-3`; the label after each heading gives the mapping.

## Global Constraints

- Python 3.11+ (per PRD Technical Approach)
- Only third-party dependencies: Streamlit, Pandas, Plotly, pytest (per PRD stack; pytest added for TDD)
- Dependencies are managed via `requirements.txt` only — no uv, no conda
- Virtual environment lives at `venv/` (already gitignored — no `.gitignore` change needed)
- Work directly on the current branch (`feature/sales-dashboard`) — no git worktree
- Code stays simple, readable, and commented (PRD NFR-3: Maintainability)
- Phase 2 items are explicitly out of scope: auth, real database, exports, alerts, filtering, drill-down, mobile-responsive design — do not build any of them
- Deployment (Streamlit Community Cloud) is executed by the user after merging to `main` — it is the last item below and is **not** an automated task in this plan

---

## Task 1: Environment Setup and Project Initialization `[TASK-1]`

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable Streamlit shell that later tasks add to.

- [ ] **Step 1: Create and activate the virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

- [ ] **Step 2: Write `requirements.txt`**

```
streamlit>=1.38
pandas>=2.2
plotly>=5.24
pytest>=8.3
```

- [ ] **Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: installs cleanly with no errors.

- [ ] **Step 4: Write the minimal `app.py`**

```python
import streamlit as st

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")
```

- [ ] **Step 5: Run the app and verify it launches**

```bash
streamlit run app.py
```

Expected: browser opens to a page titled "ShopSmart Sales Dashboard" with no errors in the terminal. Stop the server (Ctrl+C) once confirmed.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: Set up venv, dependencies, and a minimal Streamlit shell"
```

---

## Task 2: Data Loading and Validation `[TASK-2]`

**Files:**
- Create: `data_loader.py`
- Create: `tests/test_data_loader.py`
- Modify: `app.py`

**Interfaces:**
- Produces: `load_sales_data(csv_path: str) -> pd.DataFrame` — raises `FileNotFoundError` if the file doesn't exist, `ValueError` if it's empty or missing required columns. Returns a DataFrame with `date` parsed as a datetime column and columns `date, order_id, product, category, region, quantity, unit_price, total_amount`.
- Consumes: nothing from earlier tasks.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_data_loader.py
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


def test_load_sales_data_raises_on_missing_columns(tmp_path):
    csv_path = tmp_path / "bad.csv"
    csv_path.write_text("date,order_id\n2024-01-03,ORD-001\n")
    with pytest.raises(ValueError, match="missing required columns"):
        load_sales_data(str(csv_path))


def test_load_sales_data_loads_the_real_dataset():
    df = load_sales_data("data/sales-data.csv")
    assert len(df) == 482
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_data_loader.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'data_loader'`.

- [ ] **Step 3: Implement `data_loader.py`**

```python
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
        raise FileNotFoundError(f"Sales data file not found: {csv_path}")

    if df.empty:
        raise ValueError(f"Sales data file is empty: {csv_path}")

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Sales data is missing required columns: {missing}")

    df["date"] = pd.to_datetime(df["date"])
    return df
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_data_loader.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Wire data loading into `app.py`**

```python
import streamlit as st

from data_loader import load_sales_data

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

sales_df = load_sales_data("data/sales-data.csv")
st.write(f"Loaded {len(sales_df)} transactions.")
```

- [ ] **Step 6: Run the app and verify it loads real data**

```bash
streamlit run app.py
```

Expected: page shows "Loaded 482 transactions." with no errors. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add data_loader.py tests/test_data_loader.py app.py
git commit -m "TASK-2: Load and validate sales-data.csv"
```

---

## Task 3: KPI Cards `[TASK-3]`

**Files:**
- Create: `metrics.py`
- Create: `formatting.py`
- Create: `tests/test_metrics.py`
- Create: `tests/test_formatting.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: `load_sales_data` from Task 2 (returns a DataFrame with `order_id`, `total_amount` columns, among others).
- Produces: `total_sales(df) -> float`, `total_orders(df) -> int`, `format_currency(amount: float) -> str`, `format_number(n: int) -> str`. Later tasks (4, 5) add more functions to `metrics.py` alongside these.

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_metrics.py
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
```

```python
# tests/test_formatting.py
from formatting import format_currency, format_number


def test_format_currency_adds_dollar_sign_and_separators():
    assert format_currency(116543.21) == "$116,543"


def test_format_currency_rounds_to_whole_dollars():
    assert format_currency(99.6) == "$100"


def test_format_number_adds_thousands_separators():
    assert format_number(482) == "482"
    assert format_number(1234567) == "1,234,567"
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_metrics.py tests/test_formatting.py -v
```

Expected: FAIL with `ModuleNotFoundError` for both `metrics` and `formatting`.

- [ ] **Step 3: Implement `metrics.py`**

```python
"""Sales aggregation functions. Each takes the DataFrame from data_loader
and returns a small, chart-ready result — no Streamlit or plotting here."""
import pandas as pd


def total_sales(df: pd.DataFrame) -> float:
    """Sum of all transaction revenue."""
    return float(df["total_amount"].sum())


def total_orders(df: pd.DataFrame) -> int:
    """Count of unique transactions."""
    return int(df["order_id"].nunique())
```

- [ ] **Step 4: Implement `formatting.py`**

```python
"""Small display-formatting helpers, kept separate so they're easy to test
and reuse across KPI cards."""


def format_currency(amount: float) -> str:
    """Format a dollar amount as $X,XXX,XXX, rounded to whole dollars."""
    return f"${amount:,.0f}"


def format_number(n: int) -> str:
    """Format an integer with thousands separators."""
    return f"{n:,}"
```

- [ ] **Step 5: Run tests to verify they pass**

```bash
pytest tests/test_metrics.py tests/test_formatting.py -v
```

Expected: 6 passed.

- [ ] **Step 6: Wire KPI cards into `app.py`**

```python
import streamlit as st

from data_loader import load_sales_data
from metrics import total_sales, total_orders
from formatting import format_currency, format_number

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

sales_df = load_sales_data("data/sales-data.csv")

col1, col2 = st.columns(2)
col1.metric("Total Sales", format_currency(total_sales(sales_df)))
col2.metric("Total Orders", format_number(total_orders(sales_df)))
```

- [ ] **Step 7: Run the app and verify the KPI values**

```bash
streamlit run app.py
```

Expected: "Total Sales" reads approximately **$116,500** and "Total Orders" reads **482**, matching the PRD's Expected Output table. Stop the server once confirmed.

- [ ] **Step 8: Commit**

```bash
git add metrics.py formatting.py tests/test_metrics.py tests/test_formatting.py app.py
git commit -m "TASK-3: Add Total Sales and Total Orders KPI cards"
```

---

## Task 4: Sales Trend Chart `[TASK-4]`

**Files:**
- Modify: `metrics.py`
- Modify: `tests/test_metrics.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: the `sales_df` DataFrame (has `date`, `total_amount` columns).
- Produces: `sales_over_time(df, freq: str = "ME") -> pd.DataFrame` with columns `["period", "total_amount"]`, sorted chronologically.

- [ ] **Step 1: Write the failing test**

```python
# add to tests/test_metrics.py
from metrics import sales_over_time


def test_sales_over_time_groups_by_month_and_sums():
    df = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-05", "2024-01-20", "2024-02-01"]),
        "total_amount": [10.0, 20.0, 5.0],
    })
    result = sales_over_time(df, freq="ME")
    assert list(result["total_amount"]) == [30.0, 5.0]
    assert len(result) == 2
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_metrics.py::test_sales_over_time_groups_by_month_and_sums -v
```

Expected: FAIL with `ImportError: cannot import name 'sales_over_time'`.

- [ ] **Step 3: Add `sales_over_time` to `metrics.py`**

```python
# append to metrics.py
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
```

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_metrics.py -v
```

Expected: all pass, including the new test.

- [ ] **Step 5: Add the trend chart to `app.py`**

```python
# add near the top, with the other imports
import plotly.express as px
from metrics import total_sales, total_orders, sales_over_time

# add below the KPI cards block
st.subheader("Sales Trend Over Time")
trend_df = sales_over_time(sales_df)
fig_trend = px.line(trend_df, x="period", y="total_amount", markers=True)
fig_trend.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
st.plotly_chart(fig_trend, use_container_width=True)
```

Note: Plotly Express charts show exact values on hover by default — no extra code is needed to satisfy FR-2's "interactive tooltips" requirement.

- [ ] **Step 6: Run the app and verify the chart**

```bash
streamlit run app.py
```

Expected: a line chart appears below the KPIs, one point per month across the 12-month range, and hovering a point shows its exact sales value. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add metrics.py tests/test_metrics.py app.py
git commit -m "TASK-4: Add sales trend line chart"
```

---

## Task 5: Category and Region Breakdowns `[TASK-5]`

**Files:**
- Modify: `metrics.py`
- Modify: `tests/test_metrics.py`
- Modify: `app.py`

**Interfaces:**
- Consumes: the `sales_df` DataFrame (has `category`, `region`, `total_amount` columns).
- Produces: `sales_by_category(df) -> pd.DataFrame` with columns `["category", "total_amount"]`, and `sales_by_region(df) -> pd.DataFrame` with columns `["region", "total_amount"]` — both sorted highest to lowest.

- [ ] **Step 1: Write the failing tests**

```python
# add to tests/test_metrics.py
from metrics import sales_by_category, sales_by_region


def test_sales_by_category_sums_and_sorts_descending():
    df = pd.DataFrame({
        "category": ["Audio", "Electronics", "Audio"],
        "total_amount": [10.0, 50.0, 5.0],
    })
    result = sales_by_category(df)
    assert list(result["category"]) == ["Electronics", "Audio"]
    assert list(result["total_amount"]) == [50.0, 15.0]


def test_sales_by_region_sums_and_sorts_descending():
    df = pd.DataFrame({
        "region": ["South", "North", "South"],
        "total_amount": [10.0, 50.0, 5.0],
    })
    result = sales_by_region(df)
    assert list(result["region"]) == ["North", "South"]
    assert list(result["total_amount"]) == [50.0, 15.0]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_metrics.py -v
```

Expected: the two new tests FAIL with `ImportError`.

- [ ] **Step 3: Add both functions to `metrics.py`**

```python
# append to metrics.py
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Total sales per product category, sorted highest to lowest."""
    return (
        df.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Total sales per region, sorted highest to lowest."""
    return (
        df.groupby("region")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_metrics.py -v
```

Expected: all pass.

- [ ] **Step 5: Add both bar charts to `app.py`**

```python
# add near the top, with the other metrics import
from metrics import (
    total_sales, total_orders, sales_over_time,
    sales_by_category, sales_by_region,
)

# add below the trend chart block
st.subheader("Sales by Category and Region")
col3, col4 = st.columns(2)

category_df = sales_by_category(sales_df)
fig_category = px.bar(category_df, x="category", y="total_amount")
fig_category.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
col3.plotly_chart(fig_category, use_container_width=True)

region_df = sales_by_region(sales_df)
fig_region = px.bar(region_df, x="region", y="total_amount")
fig_region.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
col4.plotly_chart(fig_region, use_container_width=True)
```

- [ ] **Step 6: Run the app and verify both charts**

```bash
streamlit run app.py
```

Expected: two bar charts side by side. Category chart shows all 5 categories with **Electronics tallest**, matching the PRD's Expected Output. Region chart shows all 4 regions (North, South, East, West). Both sorted highest to lowest, with hover tooltips. Stop the server once confirmed.

- [ ] **Step 7: Commit**

```bash
git add metrics.py tests/test_metrics.py app.py
git commit -m "TASK-5: Add category and region breakdown charts"
```

---

## Task 6: Testing and Refinement `[TASK-6]`

**Files:**
- Modify: `app.py`

**Interfaces:**
- Consumes: everything built in Tasks 2–5. No new functions are produced — this task verifies and polishes what exists.

- [ ] **Step 1: Run the full automated test suite**

```bash
pytest -v
```

Expected: every test from Tasks 2–5 passes (13 tests total), with no warnings printed.

- [ ] **Step 2: Walk the PRD's acceptance criteria one by one**

Run `streamlit run app.py` and check each item from the PRD's Acceptance Criteria section and TASKS.md's TASK-6:
- [ ] KPIs visible: Total Sales and Total Orders displayed prominently
- [ ] Trend chart works: line chart shows sales over time with correct data
- [ ] Category chart works: bar chart sorted highest to lowest, all 5 categories
- [ ] Region chart works: bar chart sorted highest to lowest, all 4 regions
- [ ] Data loads correctly: values match ~$116,500 / 482 orders / Electronics on top
- [ ] No errors: terminal shows no errors or warnings while the app runs
- [ ] Professional appearance: suitable for an executive presentation

- [ ] **Step 3: Check the performance NFRs**

With the app running, reload the page and time it informally (or use the browser's Network tab). Expected: full dashboard visible within 5 seconds; each chart rendered within 2 seconds of the data loading (PRD NFR-1).

- [ ] **Step 4: Polish labels and layout in `app.py`**

Add a page icon and a short caption so the page reads as a finished dashboard, not a work-in-progress:

```python
# change the st.set_page_config call at the top of app.py
st.set_page_config(
    page_title="ShopSmart Sales Dashboard",
    page_icon="📊",
    layout="wide",
)
st.title("ShopSmart Sales Dashboard")
st.caption("Sales performance overview — updated from the latest sales data export.")
```

Remove the placeholder `st.write(f"Loaded {len(sales_df)} transactions.")` line from Task 2 if it's still present — it was only there to confirm loading worked before the KPI cards existed.

- [ ] **Step 5: Re-run the app once more to confirm the polish didn't break anything**

```bash
streamlit run app.py
```

Expected: same charts and KPI values as before, now with a page icon and caption, no errors. Stop the server once confirmed.

- [ ] **Step 6: Commit**

```bash
git add app.py
git commit -m "TASK-6: Verify acceptance criteria and polish dashboard presentation"
```

---

## TASK-7: Deployment — you run this step

This step is **not part of automated task execution** — you deploy it yourself after this branch is merged to `main`, per your ground rules. The plan stops here and hands off.

When you're ready:

1. Merge `feature/sales-dashboard` into `main` (your usual PR/merge process).
2. In Streamlit Community Cloud, create a new app pointing at this repo's `main` branch, with **Main file path** set to `app.py`. It auto-detects `requirements.txt` for dependencies.
3. Deploy, then open the public URL and re-check the same acceptance criteria from Task 6 (Step 2) against the live app.
4. Confirm the deployed version matches what you tested locally — same KPI values, same charts, same data.
5. Fill in the `Commit:` line for `TASK-7` in `TASKS.md` and move it to Done.
