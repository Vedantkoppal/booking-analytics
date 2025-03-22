from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.io as pio
from app.core.data import df

# Create router
router = APIRouter()

### ===============================
### 1. Distribution of Booking Lead Time
### ===============================
@router.get("/get_lead_time_distribution", response_class=HTMLResponse)
def get_lead_time_distribution():
    if "lead_time" in df.columns:
        fig = px.histogram(
            df,
            x="lead_time",
            nbins=50,
            title="Distribution of Booking Lead Time",
            labels={"lead_time": "Lead Time (Days)", "count": "Number of Bookings"},
            color_discrete_sequence=["skyblue"],
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>Lead time column not found in the dataset.</p>"

    return HTMLResponse(content=graph_html)

### ===============================
### 2. Average Lead Time by Customer Type
### ===============================
@router.get("/get_lead_time_by_customer_type", response_class=HTMLResponse)
def get_lead_time_by_customer_type():
    if "lead_time" in df.columns and "customer_type" in df.columns:
        avg_lead_time = df.groupby("customer_type")["lead_time"].mean().reset_index()
        fig = px.bar(
            avg_lead_time,
            x="customer_type",
            y="lead_time",
            title="Average Lead Time by Customer Type",
            labels={"customer_type": "Customer Type", "lead_time": "Average Lead Time (Days)"},
            color="lead_time",
            color_continuous_scale="Blues",
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>Required columns not found in the dataset.</p>"

    return HTMLResponse(content=graph_html)

### ===============================
### 3. Average Lead Time by Hotel Type
### ===============================
@router.get("/get_lead_time_by_hotel_type", response_class=HTMLResponse)
def get_lead_time_by_hotel_type():
    if "lead_time" in df.columns and "hotel" in df.columns:
        avg_lead_time_hotel = df.groupby("hotel")["lead_time"].mean().reset_index()
        fig = px.bar(
            avg_lead_time_hotel,
            x="hotel",
            y="lead_time",
            title="Average Lead Time by Hotel Type",
            labels={"hotel": "Hotel Type", "lead_time": "Average Lead Time (Days)"},
            color="lead_time",
            color_continuous_scale="magenta",
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>Required columns not found in the dataset.</p>"

    return HTMLResponse(content=graph_html)


### ========================================================
### 4. Lead Time Distribution for Canceled vs. Non-Canceled
### ========================================================
@router.get("/get_lead_time_cancel_vs_non_cancel", response_class=HTMLResponse)
def get_lead_time_cancel_vs_non_cancel():
    if "lead_time" in df.columns and "is_canceled" in df.columns:
        # canceled_lead_time = df[df["is_canceled"] == 1]["lead_time"]
        # non_canceled_lead_time = df[df["is_canceled"] == 0]["lead_time"]

        # Create histogram plot using Plotly
        fig = px.histogram(
            df,
            x="lead_time",
            color="is_canceled",
            nbins=50,
            title="Lead Time Distribution for Canceled vs. Non-Canceled Bookings",
            labels={"lead_time": "Lead Time (Days)", "count": "Number of Bookings"},
            color_discrete_map={1: "red", 0: "green"},
            barmode="overlay",
        )
        fig.update_traces(opacity=0.6)

        # Generate HTML for iframe
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>Required columns not found in the dataset.</p>"

    return HTMLResponse(content=graph_html)
