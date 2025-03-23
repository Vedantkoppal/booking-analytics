

import pandas as pd
import plotly.express as px
import plotly.io as pio
import json
from app.core.data_config import GROUPED_DATA
# Paths to data
REVENUE_DATA_PATH = GROUPED_DATA

# Load grouped revenue data from JSON
revenue_data = None
with open(REVENUE_DATA_PATH, "r") as f:
    revenue_data = json.load(f)


# ### =======================
# ### REVENUE GRAPH FUNCTIONS
# ### =======================


def generate_monthly_graph(year):
    df = pd.DataFrame(revenue_data["monthly"])
    df = df[df["arrival_date_year"] == int(year)]

    if df.empty:
        return "<p>No data available for the selected year.</p>"

    fig = px.line(
        df,
        x="arrival_date_month",
        y="total_revenue",
        title=f"Monthly Revenue Trend for {year}",
    )

    # ✅ Use full_html=True to include the required Plotly script
    # return pio.to_html(fig, full_html=True, include_plotlyjs="cdn")#works2
    return pio.to_html(fig, full_html=True, include_plotlyjs="cdn")


def generate_granular_graph(year, month, granularity):
    df = pd.DataFrame(revenue_data["daily" if granularity == "daily" else "weekly"])
    df = df[(df["arrival_date_year"] == int(year)) & (df["arrival_date_month"] == month)]

    if df.empty:
        return "<p>No data available for the selected month.</p>"

    fig = px.line(
        df,
        x="arrival_date_day_of_month" if granularity == "daily" else "week_of_month",
        y="total_revenue",
        title=f"{granularity.capitalize()} Revenue Trend for {month}/{year}",
    )

    # ✅ Use full_html=True here too
    # return pio.to_html(fig, full_html=True, include_plotlyjs="cdn")&&works2
    return pio.to_html(fig, full_html=True, include_plotlyjs="cdn")


