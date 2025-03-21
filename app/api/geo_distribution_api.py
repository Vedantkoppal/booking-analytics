from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Create router
router = APIRouter()

# Load data (replace with your path)
from app.core.data import df

### ================================
### Geographical Distribution API
### ================================
@router.get("/get_geo_distribution", response_class=HTMLResponse)
def get_geo_distribution():
    if "country" in df.columns:
        # Count bookings by country
        country_bookings = df["country"].value_counts().reset_index()
        country_bookings.columns = ["country", "num_bookings"]

        # Create choropleth map using Plotly
        fig = px.choropleth(
            country_bookings,
            locations="country",
            locationmode="ISO-3",
            color="num_bookings",
            title="Geographical Distribution of Bookings",
            labels={"num_bookings": "Number of Bookings"},
            color_continuous_scale="viridis",
        )

        # Generate HTML for iframe
        graph_html = pio.to_html(fig, full_html=True, include_plotlyjs="cdn")
    else:
        graph_html = "<p>Country column not found in the dataset.</p>"

    return HTMLResponse(content=graph_html)
