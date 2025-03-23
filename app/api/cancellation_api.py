from fastapi import APIRouter, Query, Depends
from fastapi.responses import HTMLResponse
import plotly.express as px 
import plotly.io as pio
from sqlalchemy import text
from app.core.data_config import get_db

# Create router
router = APIRouter()


### ============================
### 1. Overall Cancellation Rate
### ============================
@router.get("/get_cancellation_rate", response_class=HTMLResponse)
def get_cancellation_rate(db=Depends(get_db)):
    result = db.execute(text("SELECT COUNT(*) FROM my_table"))
    total_bookings = result.scalar()

    result = db.execute(text("SELECT COUNT(*) FROM my_table WHERE is_canceled = 1"))
    canceled_bookings = result.scalar()

    if total_bookings > 0:
        cancellation_rate = (canceled_bookings / total_bookings) * 100
        html_content = f"<h4 style='color: #B0B0C3;'>Cancellation Rate: <span style='color: #FF5733;'>{cancellation_rate:.2f}%</span></h4>"
    else:
        html_content = "<p>No data available.</p>"

    return HTMLResponse(content=html_content)

### =====================================
### 2. Monthly & Yearly Cancellation Rate
### =====================================
@router.get("/get_monthly_yearly_cancellation", response_class=HTMLResponse)
def get_monthly_yearly_cancellation(db=Depends(get_db)):
    # Monthly cancellation rate
    result = db.execute(text("""
        SELECT arrival_date_month, AVG(is_canceled) * 100 AS cancel_rate
        FROM my_table GROUP BY arrival_date_month
    """))
    monthly_data = result.fetchall()

    # Yearly cancellation rate
    result = db.execute(text("""
        SELECT arrival_date_year, AVG(is_canceled) * 100 AS cancel_rate
        FROM my_table GROUP BY arrival_date_year
    """))
    yearly_data = result.fetchall()

    # Plot data
    monthly_fig = px.bar(
        x=[row[0] for row in monthly_data],
        y=[row[1] for row in monthly_data],
        title="Monthly Cancellation Rate (%)",
        labels={"x": "Month", "y": "Cancellation Rate (%)"},
    )

    yearly_fig = px.bar(
        x=[row[0] for row in yearly_data],
        y=[row[1] for row in yearly_data],
        title="Yearly Cancellation Rate (%)",
        labels={"x": "Year", "y": "Cancellation Rate (%)"},
    )

    monthly_html = pio.to_html(monthly_fig, full_html=False, include_plotlyjs="cdn")
    yearly_html = pio.to_html(yearly_fig, full_html=False, include_plotlyjs="cdn")

    html_content = f"""
    <div style="display: flex; justify-content: space-around;">
        <div style="width: 48%;">{monthly_html}</div>
        <div style="width: 48%;">{yearly_html}</div>
    </div>
    """
    return HTMLResponse(content=html_content)

### =================================
### 3. Geographical Cancellation Rate
### =================================
@router.get("/get_geo_cancellation", response_class=HTMLResponse)
def get_geo_cancellation(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT country, AVG(is_canceled) * 100 AS cancel_rate
        FROM my_table
        GROUP BY country
    """))
    geo_data = result.fetchall()

    if geo_data:
        # Unpack data into lists
        countries, cancel_rates = zip(*geo_data)

        # Create choropleth map using Plotly with lists
        geo_fig = px.choropleth(
            dict(
                country=countries,
                cancel_rate=cancel_rates
            ),
            locations="country",
            locationmode="ISO-3",
            color="cancel_rate",
            title="Cancellation Rate by Country (%)",
            labels={"cancel_rate": "Cancellation Rate (%)"},
        )
        geo_html = pio.to_html(geo_fig, full_html=True, include_plotlyjs="cdn")
    else:
        geo_html = "<p>No data available for countries.</p>"

    return HTMLResponse(content=geo_html)

# =============================
# 4. Last-Minute Cancellations
# =============================
@router.get("/get_last_minute_cancellation", response_class=HTMLResponse)
def get_last_minute_cancellation(db=Depends(get_db), threshold: int = Query(2, description="Days before arrival")):
    result = db.execute(text(f"""
        SELECT COUNT(*) FROM my_table
        WHERE is_canceled = 1 AND lead_time <= {threshold}
    """))
    last_minute_cancellations = result.scalar()

    result = db.execute(text("SELECT COUNT(*) FROM my_table WHERE is_canceled = 1"))
    total_cancellations = result.scalar()

    if total_cancellations > 0:
        last_minute_rate = (last_minute_cancellations / total_cancellations) * 100
        fig = px.pie(
            names=["Last-Minute Cancellations", "Other Cancellations"],
            values=[last_minute_cancellations, total_cancellations - last_minute_cancellations],
            title=f"Last-Minute Cancellations (within {threshold} days)",
        )
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

        summary_html = f"""
        <div style="margin-top: 10px;">
            <h4 style='color: #B0B0C3;'>Last-Minute Cancellation Rate: <span style='color: #FF5733;'>{last_minute_rate:.2f}%</span></h4>
        </div>
        {graph_html}
        """
    else:
        summary_html = "<p>No cancellation data available.</p>"

    return HTMLResponse(content=summary_html)


# ===================================
# 5. Cancellation Rate by Customer Type
# ===================================
@router.get("/get_cancellation_rate_customer", response_class=HTMLResponse)
def get_cancellation_rate_customer(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT customer_type, AVG(is_canceled) * 100 AS cancel_rate
        FROM my_table GROUP BY customer_type
    """))
    customer_data = result.fetchall()

    fig = px.bar(
        x=[row[0] for row in customer_data],
        y=[row[1] for row in customer_data],
        title="Cancellation Rate by Customer Type",
        labels={"x": "Customer Type", "y": "Cancellation Rate (%)"},
        color=[row[1] for row in customer_data],
        color_continuous_scale="Magenta",
    )
    graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

    return HTMLResponse(content=graph_html)


# ===============================================
# 6. Impact of Special Requests on Cancellations
# ===============================================
@router.get("/get_special_requests_cancellation", response_class=HTMLResponse)
def get_special_requests_cancellation(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT is_canceled, AVG(total_of_special_requests) AS avg_requests
        FROM my_table GROUP BY is_canceled
    """))
    request_data = result.fetchall()

    fig = px.bar(
        x=["Not Canceled", "Canceled"],
        y=[row[1] for row in request_data],
        title="Average Number of Special Requests: Canceled vs. Non-Canceled",
        labels={"x": "Booking Status", "y": "Average Special Requests"},
        color=[row[1] for row in request_data],
        color_continuous_scale="Reds",
    )
    graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

    return HTMLResponse(content=graph_html)


# ===================================
# 7. Cancellation Rate by Market Segment
# ===================================
@router.get("/get_cancellation_rate_segment", response_class=HTMLResponse)
def get_cancellation_rate_segment(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT market_segment, AVG(is_canceled) * 100 AS cancel_rate
        FROM my_table GROUP BY market_segment
    """))
    segment_data = result.fetchall()

    fig = px.bar(
        x=[row[0] for row in segment_data],
        y=[row[1] for row in segment_data],
        title="Cancellation Rate by Market Segment",
        labels={"x": "Market Segment", "y": "Cancellation Rate (%)"},
        color=[row[1] for row in segment_data],
        color_continuous_scale="Oranges",
    )
    graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

    return HTMLResponse(content=graph_html)


# ===========================================
# 8. Weekend vs. Weekday Booking Patterns
# ===========================================
@router.get("/get_weekend_weekday_patterns", response_class=HTMLResponse)
def get_weekend_weekday_patterns(db=Depends(get_db)):
    result = db.execute(text("SELECT SUM(stays_in_weekend_nights) FROM my_table"))
    total_weekend_bookings = result.scalar()

    result = db.execute(text("SELECT SUM(stays_in_week_nights) FROM my_table"))
    total_weekday_bookings = result.scalar()

    fig = px.bar(
        x=["Weekdays", "Weekends"],
        y=[total_weekday_bookings, total_weekend_bookings],
        title="Weekend vs. Weekday Booking Patterns",
        labels={"x": "Booking Type", "y": "Number of Nights Booked"},
        color=["Weekdays", "Weekends"],
        color_discrete_map={"Weekdays": "skyblue", "Weekends": "orange"},
    )
    graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")

    return HTMLResponse(content=graph_html)