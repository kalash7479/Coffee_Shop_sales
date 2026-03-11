import streamlit as st
import pandas as pd
import plotly.express as px
import Vis

# ---------------------------------------------------------
# 1. Load Data Function
# ---------------------------------------------------------
def load_data(path):
    df = pd.read_csv(path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['transaction_date'] = pd.to_datetime(
        df['transaction_date'],
        format='%m/%d/%Y',
        errors='coerce'
    )
    df['transaction_time'] = pd.to_datetime(
        df['transaction_time'],
        format='%H:%M:%S',
        errors='coerce'
    ).dt.time
    df['transaction_hour'] = pd.to_datetime(
        df['transaction_time'].astype(str), format='%H:%M:%S', errors='coerce'
    ).dt.hour
    return df

# ---------------------------------------------------------
# 2. Helper: Aggregate data for time-series charts
# ---------------------------------------------------------
def aggregate(df, feature, granularity):
    """
    Returns a resampled Series with PeriodIndex
    so Vis functions can use .index.start_time
    """
    ts = df.set_index('transaction_date')[feature]
    freq_map = {'Daily': 'D', 'Weekly': 'W', 'Monthly': 'ME'}
    freq = freq_map.get(granularity, 'ME')

    if feature == 'transaction_id':
        return ts.resample(freq).count().to_period(freq[0])
    else:
        return ts.resample(freq).sum().to_period(freq[0])

# ---------------------------------------------------------
# 3. Load Dataset
# ---------------------------------------------------------
df = load_data('CoffeeShopSales.csv')

# ---------------------------------------------------------
# 4. Streamlit UI Setup
# ---------------------------------------------------------
st.set_page_config(page_title="Coffee Shop Sales Dashboard", layout="wide")
st.title("☕ Coffee Shop Sales Dashboard")

# ---------------------------------------------------------
# 5. Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

min_date = df['transaction_date'].min()
max_date = df['transaction_date'].max()

selected_date = st.sidebar.date_input(
    "Select Date Range", value=(min_date, max_date)
)

granularity = st.sidebar.selectbox(
    "Granularity", ["Daily", "Weekly", "Monthly"], index=2
)

feature = st.sidebar.selectbox(
    "Metric", ["unit_price", "transaction_qty", "transaction_id"],
    format_func=lambda x: {
        "unit_price": "Total Sales ($)",
        "transaction_qty": "Units Sold",
        "transaction_id": "Number of Transactions"
    }[x]
)

filtered_df = df[
    (df['transaction_date'] >= pd.to_datetime(selected_date[0])) &
    (df['transaction_date'] <= pd.to_datetime(selected_date[1]))
]

# ---------------------------------------------------------
# 6. KPIs
# ---------------------------------------------------------
st.subheader("📌 Key Performance Indicators")

kpi1 = filtered_df['unit_price'].sum()
kpi2 = filtered_df['transaction_qty'].sum()
kpi3 = round(kpi1 / kpi2, 2) if kpi2 > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales ($)", f"{kpi1:,.2f}")
col2.metric("Total Units Sold", f"{kpi2:,}")
col3.metric("Avg Ticket Size ($)", f"{kpi3}")

# ---------------------------------------------------------
# 7. Sales Trends
# ---------------------------------------------------------
st.subheader("📊 Sales Trends")

aggregated = aggregate(filtered_df, feature, granularity)

colA, colB = st.columns(2)
with colA:
    st.plotly_chart(
        Vis.bar_chart(aggregated, granularity, feature),
        use_container_width=True
    )
with colB:
    st.plotly_chart(
        Vis.line_chart(aggregated, granularity, feature),
        use_container_width=True
    )

# ---------------------------------------------------------
# 8. Category Breakdown
# ---------------------------------------------------------
st.subheader("📂 Category Breakdown")

category_data = (
    filtered_df.groupby('product_category')['unit_price']
    .sum()
    .reset_index()
    .set_index('product_category')
)
st.plotly_chart(
    Vis.category_breakdown(category_data, 'unit_price'),
    use_container_width=True
)

# ---------------------------------------------------------
# 9. Top Selling Products
# ---------------------------------------------------------
st.subheader("🏆 Top Selling Products")

top_products = (
    filtered_df.groupby('product_type')['unit_price']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
st.plotly_chart(
    Vis.top_selling_product(top_products),
    use_container_width=True
)

# ---------------------------------------------------------
# 10. Hourly Sales
# ---------------------------------------------------------
st.subheader("⏱️ Sales by Hour of Day")

hourly = (
    filtered_df.groupby(
        [filtered_df['transaction_date'].dt.date, 'transaction_hour']
    )['unit_price'].sum()
    .reset_index()
    .groupby('transaction_hour')['unit_price'].mean()
)
st.plotly_chart(
    Vis.avg_sales_by_hourofday(hourly, 'Sales'),
    use_container_width=True
)

# ---------------------------------------------------------
st.success("Dashboard Loaded Successfully!")
