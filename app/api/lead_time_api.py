from fastapi import APIRouter,Depends
from fastapi.responses import HTMLResponse
import plotly.express as px
import plotly.io as pio
# /from app.core.data_config import df
from sqlalchemy import text
from app.core.data_config import get_db

# Create router
router = APIRouter()

### ===============================
### 1. Distribution of Booking Lead Time
### ===============================
@router.get("/get_lead_time_distribution", response_class=HTMLResponse)
def get_lead_time_distribution(db=Depends(get_db)):
    result = db.execute(text("SELECT lead_time FROM my_table"))
    lead_time_data = [row[0] for row in result.fetchall()]
    if lead_time_data:
        fig = px.histogram(
            x=lead_time_data,
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
def get_lead_time_by_customer_type(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT customer_type, AVG(lead_time) AS avg_lead_time
        FROM my_table
        GROUP BY customer_type
    """))
    data = result.fetchall()
    # if "lead_time" in df.columns and "customer_type" in df.columns:
    #     avg_lead_time = df.groupby("customer_type")["lead_time"].mean().reset_index()
    if data:
        customer_type_data = [row[0] for row in data]
        avg_lead_time_data = [row[1] for row in data]
        fig = px.bar(
            x=customer_type_data,
            y=avg_lead_time_data,
            title="Average Lead Time by Customer Type",
            labels={"customer_type": "Customer Type", "lead_time": "Average Lead Time (Days)"},
            color=avg_lead_time_data,
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
def get_lead_time_by_hotel_type(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT hotel, AVG(lead_time) AS avg_lead_time
        FROM my_table
        GROUP BY hotel
    """))
    data = result.fetchall()

    if data:
        hotel_data = [row[0] for row in data]
        avg_lead_time_data = [row[1] for row in data]

        fig = px.bar(
            x=hotel_data,
            y=avg_lead_time_data,
            title="Average Lead Time by Hotel Type",
            labels={"x": "Hotel Type", "y": "Average Lead Time (Days)"},
            color=avg_lead_time_data,
            color_continuous_scale="magenta",
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>No data found.</p>"

    return HTMLResponse(content=graph_html)


### ========================================================
### 4. Lead Time Distribution for Canceled vs. Non-Canceled
### ========================================================
@router.get("/get_lead_time_cancel_vs_non_cancel", response_class=HTMLResponse)
def get_lead_time_cancel_vs_non_cancel(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT lead_time, is_canceled
        FROM my_table
    """))
    data = result.fetchall()

    if data:
        lead_time_data = [row[0] for row in data]
        is_canceled_data = ["Canceled" if row[1] == 1 else "Non-Canceled" for row in data]

        # Plotly histogram
        fig = px.histogram(
            x=lead_time_data,
            color=is_canceled_data,
            nbins=50,
            title="Lead Time Distribution for Canceled vs. Non-Canceled Bookings",
            labels={"x": "Lead Time (Days)", "y": "Number of Bookings"},
            color_discrete_map={"Canceled": "red", "Non-Canceled": "green"},
            barmode="overlay",
        )
        fig.update_traces(opacity=0.6)
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>No data found.</p>"

    return HTMLResponse(content=graph_html)
