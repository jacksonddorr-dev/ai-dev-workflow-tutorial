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
