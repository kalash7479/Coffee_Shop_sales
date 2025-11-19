import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# -------------------------
# BAR CHART
# -------------------------
def bar_chart(df, x_col, y_col):
    df = df.copy()
    df[x_col] = df[x_col].astype(str)

    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col.replace('_', ' ').title()} by {x_col.replace('_', ' ').title()}",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


# -------------------------
# LINE CHART
# -------------------------
def line_chart(df, x_col, y_col):
    df = df.copy()
    df = df.sort_values(x_col)
    df[x_col] = df[x_col].astype(str)

    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        markers=True,
        title=f"{y_col.replace('_', ' ').title()} Trend by {x_col.replace('_', ' ').title()}",
        template="plotly_white"
    )
    return fig


# -------------------------
# SALES BY DAY (Daily Trend)
# -------------------------
def daily_sales_trend(df, date_col, sales_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    daily = df.groupby(date_col)[sales_col].sum().reset_index()

    fig = px.line(
        daily,
        x=date_col,
        y=sales_col,
        title="Daily Sales Trend",
        markers=True,
        template="plotly_white"
    )
    return fig


# -------------------------
# MONTHLY SALES TREND
# -------------------------
def monthly_sales(df, date_col, sales_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df["Month"] = df[date_col].dt.to_period("M").astype(str)

    monthly = df.groupby("Month")[sales_col].sum().reset_index()

    fig = px.line(
        monthly,
        x="Month",
        y=sales_col,
        title="Monthly Sales Trend",
        markers=True,
        template="plotly_white"
    )
    return fig


# -------------------------
# AVERAGE SALES BY HOUR OF DAY
# -------------------------
def avg_sales_by_hour(df, time_col, sales_col):
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])
    df["Hour"] = df[time_col].dt.hour

    hourly = df.groupby("Hour")[sales_col].mean().reset_index()

    fig = px.line(
        hourly,
        x="Hour",
        y=sales_col,
        markers=True,
        title="Average Sales by Hour of Day",
        template="plotly_white"
    )
    return fig


# -------------------------
# TOP N PRODUCTS SOLD
# -------------------------
def top_selling_products(df, product_col, qty_col, n=10):
    df = df.copy()
    top = df.groupby(product_col)[qty_col].sum().nlargest(n).reset_index()

    fig = px.bar(
        top,
        x=product_col,
        y=qty_col,
        title=f"Top {n} Best Selling Products",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


# -------------------------
# CATEGORY SALES BREAKDOWN
# -------------------------
def category_breakdown(df, category_col, sales_col):
    category = df.groupby(category_col)[sales_col].sum().reset_index()

    fig = px.pie(
        category,
        names=category_col,
        values=sales_col,
        title="Sales Breakdown by Category"
    )
    return fig


# -------------------------
# SALES BY STORE LOCATION
# -------------------------
def store_sales(df, store_col, sales_col):
    store = df.groupby(store_col)[sales_col].sum().reset_index()

    fig = px.bar(
        store,
        x=store_col,
        y=sales_col,
        title="Sales by Store Location",
        template="plotly_white"
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig


# -------------------------
# CUSTOMER COUNT BY DAY
# -------------------------
def customers_per_day(df, date_col, customer_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])

    cust = df.groupby(date_col)[customer_col].sum().reset_index()

    fig = px.line(
        cust,
        x=date_col,
        y=customer_col,
        title="Customer Count by Day",
        markers=True,
        template="plotly_white"
    )
    return fig


# -------------------------
# WEEKLY SALES TREND
# -------------------------
def weekly_sales(df, date_col, sales_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df["Week"] = df[date_col].dt.to_period("W").astype(str)

    week = df.groupby("Week")[sales_col].sum().reset_index()

    fig = px.line(
        week,
        x="Week",
        y=sales_col,
        markers=True,
        title="Weekly Sales Trend",
        template="plotly_white"
    )
    return fig


# -------------------------
# GROWTH RATE CALCULATION
# -------------------------
def growth_rate(df, date_col, sales_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df["Month"] = df[date_col].dt.to_period("M").astype(str)

    monthly = df.groupby("Month")[sales_col].sum().reset_index()
    monthly["Growth %"] = monthly[sales_col].pct_change() * 100

    fig = px.line(
        monthly,
        x="Month",
        y="Growth %",
        markers=True,
        title="Monthly Growth Rate (%)",
        template="plotly_white"
    )
    return fig
