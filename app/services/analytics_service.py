
# import plotly.express as px
# import plotly.io as pio
# import pandas as pd
# import os

# # Define path to save the graph
# GRAPH_PATH = "app/static/graphs/revenue_trend.html"

# def generate_granular_graph(year, month, granularity):
#     df = pd.DataFrame(revenue_data["daily" if granularity == "daily" else "weekly"])
#     df = df[(df["arrival_date_year"] == int(year)) & (df["arrival_date_month"] == month)]

#     if df.empty:
#         return {"error": "No data available for the selected year and month."}

#     # ✅ Create Plotly graph
#     fig = px.line(
#         df,
#         x="arrival_date_day_of_month",
#         y="total_revenue",
#         title=f"{granularity.capitalize()} Revenue Trend for {month}/{year}",
#     )

#     # ✅ Overwrite the same graph file every time
#     pio.write_html(fig, file=GRAPH_PATH, full_html=False, include_plotlyjs="cdn")

#     # ✅ Return the path to the same graph file
#     return {"graph_path": "/static/graphs/revenue_trend.html"}














#  &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# following works

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


# ### =======================
# ### REVENUE GRAPH FUNCTIONS
# ### =======================


import plotly.express as px
import plotly.io as pio
import pandas as pd

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


# Yearly Revenue Trend Graph&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&Below works
# def generate_yearly_graph(year):
#     df = pd.DataFrame(revenue_data["yearly"])
#     df = df[df["arrival_date_year"] == int(year)]
#     print(year)

#     if df.empty:
#         return "<p>No data available for the selected year.</p>"

#     fig = px.line(df, x="arrival_date_year", y="total_revenue", title=f"Yearly Revenue Trend for {year}")
#     return {
#         "data": fig.to_dict()["data"],
#         "layout": fig.to_dict()["layout"],
#     }

# # Monthly Revenue Trend Graph
# def generate_monthly_graph(year):
#     df = pd.DataFrame(revenue_data["monthly"])
#     df = df[df["arrival_date_year"] == int(year)]

#     if df.empty:
#         return "<p>No data available for the selected year.</p>"

#     fig = px.line(
#         df,
#         x="arrival_date_month",
#         y="total_revenue",
#         title=f"Monthly Revenue Trend for {year}",
#         markers=True,
#     )
#     # graph_html = pio.to_html(fig, full_html=False)
#     return {
#         "data": fig.to_dict()["data"],
#         "layout": fig.to_dict()["layout"],
#     }



# # Daily or Weekly Revenue Graph
# def generate_granular_graph(year, month, granularity):
#     if granularity == "daily":
#         df = pd.DataFrame(revenue_data["daily"])
#         df = df[
#             (df["arrival_date_year"] == int(year))
#             & (df["arrival_date_month"] == month)
#         ]

#         if df.empty:
#             return "<p>No data available for the selected month.</p>"

#         fig = px.line(
#             df,
#             x="arrival_date_day_of_month",
#             y="total_revenue",
#             title=f"Daily Revenue Trend for {month}/{year}",
#         )
#     elif granularity == "weekly":
#         df = pd.DataFrame(revenue_data["weekly"])
#         df = df[
#             (df["arrival_date_year"] == int(year))
#             & (df["arrival_date_month"] == month)
#         ]

#         if df.empty:
#             return "<p>No data available for the selected month.</p>"

#         fig = px.bar(
#             df,
#             x="week_of_month",
#             y="total_revenue",
#             title=f"Weekly Revenue Trend for {month}/{year}",
#         )
#     else:
#         return "<p>Invalid granularity selected.</p>"

#     graph_html = pio.to_html(fig, full_html=False)
#     html_content = f'''
#         <div>
#             {graph_html}
#         </div>
#     '''
#     return {
#         "data": fig.to_dict()["data"],
#         "layout": fig.to_dict()["layout"],
#     }

