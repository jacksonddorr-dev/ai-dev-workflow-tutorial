import streamlit as st
import plotly.express as px

from data_loader import load_sales_data
from metrics import (
    total_sales, total_orders, sales_over_time,
    sales_by_category, sales_by_region,
)
from formatting import format_currency, format_number

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide", page_icon="📊")
st.title("ShopSmart Sales Dashboard")
st.caption("Sales performance overview — updated from the latest sales data export.")

try:
    sales_df = load_sales_data("data/sales-data.csv")
except (FileNotFoundError, ValueError) as e:
    st.error(f"Could not load sales data: {e}")
    st.stop()

col1, col2 = st.columns(2)
col1.metric("Total Sales", format_currency(total_sales(sales_df)))
col2.metric("Total Orders", format_number(total_orders(sales_df)))

st.subheader("Sales Trend Over Time")
trend_df = sales_over_time(sales_df)
fig_trend = px.line(trend_df, x="period", y="total_amount", markers=True)
fig_trend.update_layout(xaxis_title="Month", yaxis_title="Sales ($)")
st.plotly_chart(fig_trend, width="stretch")

st.subheader("Sales by Category and Region")
col3, col4 = st.columns(2)

category_df = sales_by_category(sales_df)
fig_category = px.bar(category_df, x="category", y="total_amount")
fig_category.update_layout(xaxis_title="Category", yaxis_title="Sales ($)")
col3.plotly_chart(fig_category, width="stretch")

region_df = sales_by_region(sales_df)
fig_region = px.bar(region_df, x="region", y="total_amount")
fig_region.update_layout(xaxis_title="Region", yaxis_title="Sales ($)")
col4.plotly_chart(fig_region, width="stretch")
