import streamlit as st
import pandas as pd
import plotly.express as px
import Vis

# ---------------------------------------------------------
# 1. Load Data Function
# ---------------------------------------------------------
def load_data(path):
    df = pd.read_csv(path)

    # Remove accidental unnamed index column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Correct date format: MM/DD/YYYY
    df['transaction_date'] = pd.to_datetime(
        df['transaction_date'],
        format='%m/%d/%Y',
        errors='coerce'
    )

    # Correct time format
    df['transaction_time'] = pd.to_datetime(
        df['transaction_time'],
        format='%H:%M:%S',
        errors='coerce'
    ).dt.time

    return df

# ---------------------------------------------------------
# 2. Load Dataset
# ---------------------------------------------------------
df = load_data('CoffeeShopSales.csv')

# ---------------------------------------------------------
# 3. Streamlit UI Setup
# ---------------------------------------------------------
st.set_page_config(page_title="Coffee Shop Sales Dashboard", layout="wide")
st.title("☕ Coffee Shop Sales Dashboard")

# ---------------------------------------------------------
# 4. Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filters")

min_date = df['transaction_date'].min()
max_date = df['transaction_date'].max()

selected_date = st.sidebar.date_input(
    "Select Date Range", value=(min_date, max_date)
)

filtered_df = df[(df['transaction_date'] >= pd.to_datetime(selected_date[0])) &
                 (df['transaction_date'] <= pd.to_datetime(selected_date[1]))]

# ---------------------------------------------------------
# 5. KPIs
# ---------------------------------------------------------
st.subheader("📌 Key Performance Indicators")

kpi1 = filtered_df['unit_price'].sum()  # Total sales
kpi2 = filtered_df['transaction_qty'].sum()  # Total quantity sold
kpi3 = round(kpi1 / kpi2, 2) if kpi2 > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales ($)", f"{kpi1:,.2f}")
col2.metric("Total Units Sold", f"{kpi2}")
col3.metric("Avg Ticket Size ($)", f"{kpi3}")

# ---------------------------------------------------------
# 6. Charts Section
# ---------------------------------------------------------
st.subheader("📊 Sales Insights")

colA, colB = st.columns(2)

with colA:
    st.plotly_chart(Vis.bar_chart(filtered_df, 'transaction_date', 'unit_price'))

with colB:
    st.plotly_chart(Vis.line_chart(filtered_df, 'transaction_date', 'unit_price'))

# ---------------------------------------------------------
# 7. Detailed Sales Breakdown
# ---------------------------------------------------------
st.subheader("📂 Category Breakdown")
st.plotly_chart(Vis.category_breakdown(filtered_df))

# ---------------------------------------------------------
# 8. Top Selling Product
# ---------------------------------------------------------
st.subheader("🏆 Top Selling Products")
st.plotly_chart(Vis.top_selling_product(filtered_df))

# ---------------------------------------------------------
# 9. Hourly Sales Heatmap
# ---------------------------------------------------------
st.subheader("⏱️ Sales by Hour of Day")
st.plotly_chart(Vis.avg_sales_by_hourofday(filtered_df))

# ---------------------------------------------------------
# END
# ---------------------------------------------------------
st.success("Dashboard Loaded Successfully!")
