import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

# Paths to data
REVENUE_DATA_PATH = "data/grouped_data.json"
DATA_PATH = "data/hotel_bookings.csv"

# Load grouped revenue data from JSON
revenue_data = None
with open(REVENUE_DATA_PATH, "r") as f:
    revenue_data = json.load(f)


### =======================
### REVENUE GRAPH FUNCTIONS
### =======================

# Yearly Revenue Trend Graph
def generate_yearly_graph(year):
    df = pd.DataFrame(revenue_data["yearly"])
    df = df[df["arrival_date_year"] == int(year)]
    print(year)

    if df.empty:
        return "<p>No data available for the selected year.</p>"

    fig = px.line(df, x="arrival_date_year", y="total_revenue", title=f"Yearly Revenue Trend for {year}")
    return pio.to_html(fig, full_html=False)

# Monthly Revenue Trend Graph
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
        markers=True,
    )
    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


# Daily or Weekly Revenue Graph
def generate_granular_graph(year, month, granularity):
    if granularity == "daily":
        df = pd.DataFrame(revenue_data["daily"])
        df = df[
            (df["arrival_date_year"] == int(year))
            & (df["arrival_date_month"] == month)
        ]

        if df.empty:
            return "<p>No data available for the selected month.</p>"

        fig = px.line(
            df,
            x="arrival_date_day_of_month",
            y="total_revenue",
            title=f"Daily Revenue Trend for {month}/{year}",
        )
    elif granularity == "weekly":
        df = pd.DataFrame(revenue_data["weekly"])
        df = df[
            (df["arrival_date_year"] == int(year))
            & (df["arrival_date_month"] == month)
        ]

        if df.empty:
            return "<p>No data available for the selected month.</p>"

        fig = px.bar(
            df,
            x="week_of_month",
            y="total_revenue",
            title=f"Weekly Revenue Trend for {month}/{year}",
        )
    else:
        return "<p>Invalid granularity selected.</p>"

    graph_html = pio.to_html(fig, full_html=False)
    html_content = f'''
        <div>
            {graph_html}
        </div>
    '''
    return html_content
    # return {
    #     "data": fig.to_dict()["data"],
    #     "layout": fig.to_dict()["layout"],
    # }
