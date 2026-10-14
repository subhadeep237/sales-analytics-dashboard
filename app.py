
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 2. LOAD CLEANED DATA
# --------------------------------------------------

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "processed"
    / "superstore_cleaned.csv"
)


@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE)

    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )

    df["sales"] = pd.to_numeric(
        df["sales"], errors="coerce"
    )

    df["profit"] = pd.to_numeric(
        df["profit"], errors="coerce"
    )

    df["order_quantity"] = pd.to_numeric(
        df["order_quantity"], errors="coerce"
    )

    return df


try:
    df = load_data()
except Exception as error:
    st.error(f"Unable to load the dataset: {error}")
    st.info(
        "Run python main.py first to generate "
        "the cleaned CSV file."
    )
    st.stop()


# --------------------------------------------------
# 3. DASHBOARD HEADER
# --------------------------------------------------

st.title("📊 Sales Analytics Dashboard")

st.markdown(
    "Explore sales performance, profitability, "
    "product categories and customer orders."
)

st.caption(
    f"Dataset: {len(df):,} records | "
    "Source: cleaned Superstore sales data"
)

st.divider()


# --------------------------------------------------
# 4. SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

st.sidebar.caption(
    "Choose filters to update the entire dashboard."
)

filtered = df.copy()

# Region filter
regions = sorted(
    df["region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

# Product category filter
categories = sorted(
    df["product_category"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=categories,
    default=categories
)

# Customer segment filter
segments = sorted(
    df["customer_segment"].dropna().unique().tolist()
)

selected_segments = st.sidebar.multiselect(
    "Select Customer Segment",
    options=segments,
    default=segments
)

# Shipping mode filter
ship_modes = sorted(
    df["ship_mode"].dropna().unique().tolist()
)

selected_ship_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    options=ship_modes,
    default=ship_modes
)

# Date filter
valid_dates = df["order_date"].dropna()

if not valid_dates.empty:
    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_dates = st.sidebar.date_input(
        "Select Order Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if isinstance(selected_dates, (tuple, list)):
        if len(selected_dates) == 2:
            start_date, end_date = selected_dates

            filtered = filtered[
                filtered["order_date"].dt.date.between(
                    start_date, end_date
                )
            ]
        elif len(selected_dates) == 1:
            selected_date = selected_dates[0]

            filtered = filtered[
                filtered["order_date"].dt.date
                == selected_date
            ]


filtered = filtered[
    filtered["region"].isin(selected_regions)
    & filtered["product_category"].isin(
        selected_categories
    )
    & filtered["customer_segment"].isin(
        selected_segments
    )
    & filtered["ship_mode"].isin(selected_ship_modes)
]


# --------------------------------------------------
# 5. HANDLE EMPTY FILTER RESULTS
# --------------------------------------------------

if filtered.empty:
    st.warning(
        "No records match these filters. "
        "Please select different filters."
    )
    st.stop()


# --------------------------------------------------
# 6. CALCULATE KEY PERFORMANCE INDICATORS
# --------------------------------------------------

total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()

total_orders = filtered["order_id"].nunique()

total_customers = filtered["customer_name"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# --------------------------------------------------
# 7. DISPLAY KPI CARDS
# --------------------------------------------------

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"{total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"{total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{total_orders:,}"
)

col4.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)

st.caption(
    f"Unique customers in current selection: "
    f"{total_customers:,}"
)

st.divider()


# --------------------------------------------------
# 8. SALES BY REGION
# --------------------------------------------------

st.subheader("Sales Performance by Region")

region_df = (
    filtered.groupby("region", as_index=False)
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum")
    )
    .sort_values("total_sales", ascending=False)
)

left, right = st.columns(2)

with left:
    fig_region = px.bar(
        region_df,
        x="region",
        y="total_sales",
        color="region",
        title="Total Sales by Region",
        labels={
            "region": "Region",
            "total_sales": "Total Sales"
        },
        template="plotly_white"
    )

    fig_region.update_layout(
        showlegend=False,
        xaxis_tickangle=-30
    )

    st.plotly_chart(
        fig_region, use_container_width=True
    )

with right:
    fig_profit_region = px.bar(
        region_df,
        x="region",
        y="total_profit",
        color="region",
        title="Total Profit by Region",
        labels={
            "region": "Region",
            "total_profit": "Total Profit"
        },
        template="plotly_white"
    )

    fig_profit_region.update_layout(
        showlegend=False,
        xaxis_tickangle=-30
    )

    st.plotly_chart(
        fig_profit_region, use_container_width=True
    )


# --------------------------------------------------
# 9. CATEGORY ANALYSIS
# --------------------------------------------------

st.divider()
st.subheader("Product Category Analysis")

category_df = (
    filtered.groupby("product_category", as_index=False)
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum")
    )
    .sort_values("total_sales", ascending=False)
)

left, right = st.columns(2)

with left:
    fig_category = px.pie(
        category_df,
        names="product_category",
        values="total_sales",
        title="Sales Share by Category",
        hole=0.45,
        template="plotly_white"
    )

    st.plotly_chart(
        fig_category, use_container_width=True
    )

with right:
    fig_category_profit = px.bar(
        category_df,
        x="product_category",
        y="total_profit",
        color="product_category",
        title="Profit by Category",
        labels={
            "product_category": "Category",
            "total_profit": "Total Profit"
        },
        template="plotly_white"
    )

    fig_category_profit.update_layout(
        showlegend=False
    )

    st.plotly_chart(
        fig_category_profit, use_container_width=True
    )


# --------------------------------------------------
# 10. MONTHLY SALES TREND
# --------------------------------------------------

st.divider()
st.subheader("Monthly Sales Trend")

monthly_df = filtered.dropna(
    subset=["order_date"]
).copy()

monthly_df["year_month"] = (
    monthly_df["order_date"].dt.to_period("M").astype(str)
)

monthly_df = (
    monthly_df.groupby("year_month", as_index=False)
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum")
    )
    .sort_values("year_month")
)

fig_monthly = px.line(
    monthly_df,
    x="year_month",
    y="total_sales",
    markers=True,
    title="Monthly Sales Over Time",
    labels={
        "year_month": "Month",
        "total_sales": "Total Sales"
    },
    template="plotly_white"
)

fig_monthly.update_layout(
    xaxis_tickangle=-45,
    hovermode="x unified"
)

st.plotly_chart(
    fig_monthly, use_container_width=True
)


# --------------------------------------------------
# 11. TOP 10 PRODUCTS
# --------------------------------------------------

st.divider()
st.subheader("Top 10 Products by Sales")

product_df = (
    filtered.groupby(
        ["product_name", "product_category"],
        as_index=False
    )
    .agg(
        total_sales=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("order_quantity", "sum")
    )
    .sort_values("total_sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    product_df.sort_values("total_sales"),
    x="total_sales",
    y="product_name",
    color="product_category",
    orientation="h",
    title="Best-Selling Products",
    labels={
        "total_sales": "Total Sales",
        "product_name": "Product",
        "product_category": "Category"
    },
    template="plotly_white"
)

st.plotly_chart(
    fig_products, use_container_width=True
)


# --------------------------------------------------
# 12. DETAILED DATA TABLE
# --------------------------------------------------

st.divider()
st.subheader("Detailed Product Performance")

display_df = product_df.rename(
    columns={
        "product_name": "Product",
        "product_category": "Category",
        "total_sales": "Total Sales",
        "total_profit": "Total Profit",
        "total_quantity": "Quantity Sold"
    }
)

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# 13. DOWNLOAD FILTERED DATA
# --------------------------------------------------

st.subheader("Export Data")

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)


# --------------------------------------------------
# 14. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Sales Analytics Dashboard | Built with "
    "Python, Pandas, Streamlit and Plotly"
)
