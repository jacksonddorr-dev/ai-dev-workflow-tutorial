import streamlit as st

from data_loader import load_sales_data

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")
st.title("ShopSmart Sales Dashboard")

sales_df = load_sales_data("data/sales-data.csv")
st.write(f"Loaded {len(sales_df)} transactions.")
