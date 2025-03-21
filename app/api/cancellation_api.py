from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Create router
router = APIRouter()

# Load data (replace with your path)
DATA_PATH = "data/updated_data.csv"
df = pd.read_csv(DATA_PATH)

### ============================
### 1. Overall Cancellation Rate
### ============================
@router.get("/get_cancellation_rate", response_class=HTMLResponse)
def get_cancellation_rate():
    if "is_canceled" in df.columns:
        total_bookings = len(df)
        canceled_bookings = df["is_canceled"].sum()
        cancellation_rate = (canceled_bookings / total_bookings) * 100
        html_content = f"<h4>Cancellation Rate: {cancellation_rate:.2f}%</h4>"
    else:
        html_content = "<p>Cancellation column not found in the dataset.</p>"

    return HTMLResponse(content=html_content)

### =====================================
### 2. Monthly & Yearly Cancellation Rate
### =====================================
@router.get("/get_monthly_yearly_cancellation", response_class=HTMLResponse)
def get_monthly_yearly_cancellation():
    if "is_canceled" in df.columns and "arrival_date_month" in df.columns and "arrival_date_year" in df.columns:
        # Monthly cancellation rate
        monthly_cancellation = df.groupby("arrival_date_month")["is_canceled"].mean() * 100
        monthly_fig = px.bar(
            x=monthly_cancellation.index,
            y=monthly_cancellation.values,
            title="Monthly Cancellation Rate (%)",
            labels={"x": "Month", "y": "Cancellation Rate (%)"},
        )

        # Yearly cancellation rate
        yearly_cancellation = df.groupby("arrival_date_year")["is_canceled"].mean() * 100
        yearly_fig = px.bar(
            x=yearly_cancellation.index,
            y=yearly_cancellation.values,
            title="Yearly Cancellation Rate (%)",
            labels={"x": "Year", "y": "Cancellation Rate (%)"},
        )

        # Generate combined HTML
        monthly_html = pio.to_html(monthly_fig, full_html=False, include_plotlyjs="cdn")
        yearly_html = pio.to_html(yearly_fig, full_html=False, include_plotlyjs="cdn")

        html_content = f"""
        <div style="display: flex; justify-content: space-around;">
            <div style="width: 48%;">{monthly_html}</div>
            <div style="width: 48%;">{yearly_html}</div>
        </div>
        """
    else:
        html_content = "<p>Required columns not found in the dataset.</p>"

    return HTMLResponse(content=html_content)

### =================================
### 3. Geographical Cancellation Rate
### =================================
@router.get("/get_geo_cancellation", response_class=HTMLResponse)
def get_geo_cancellation():
    if "country" in df.columns and "is_canceled" in df.columns:
        # Cancellation rate by country
        country_cancellation = df.groupby("country")["is_canceled"].mean() * 100
        geo_fig = px.choropleth(
            country_cancellation.reset_index(),
            locations="country",
            locationmode="ISO-3",
            color="is_canceled",
            title="Cancellation Rate by Country (%)",
            labels={"is_canceled": "Cancellation Rate (%)"},
        )
        geo_html = pio.to_html(geo_fig, full_html=True, include_plotlyjs="cdn")
    else:
        geo_html = "<p>Country or cancellation column not found in the dataset.</p>"

    return HTMLResponse(content=geo_html)

### =============================
### 4. Last-Minute Cancellations
### =============================
@router.get("/get_last_minute_cancellation", response_class=HTMLResponse)
def get_last_minute_cancellation(threshold: int = Query(2, description="Days before arrival")):
    if "is_canceled" in df.columns and "lead_time" in df.columns:
        # Filter for last-minute cancellations
        last_minute_cancellations = df[(df["is_canceled"] == 1) & (df["lead_time"] <= threshold)]
        last_minute_rate = (len(last_minute_cancellations) / df["is_canceled"].sum()) * 100

        fig = px.pie(
            names=["Last-Minute Cancellations", "Other Cancellations"],
            values=[len(last_minute_cancellations), df["is_canceled"].sum() - len(last_minute_cancellations)],
            title=f"Last-Minute Cancellations (within {threshold} days)",
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

        summary_html = f"""
        <div style="margin-top: 10px;">
            <h4>Last-Minute Cancellation Rate: {last_minute_rate:.2f}%</h4>
        </div>
        {graph_html}
        """
    else:
        summary_html = "<p>Required columns not found in the dataset.</p>"

    return HTMLResponse(content=summary_html)
