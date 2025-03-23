from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
import plotly.express as px
import plotly.io as pio
from sqlalchemy import text
from app.core.data_config import get_db

# Create router
router = APIRouter()

### ================================
### Geographical Distribution API
### ================================
@router.get("/get_geo_distribution", response_class=HTMLResponse)
def get_geo_distribution(db=Depends(get_db)):
    result = db.execute(text("""
        SELECT country, COUNT(*) AS num_bookings
        FROM my_table
        GROUP BY country
    """))
    geo_data = result.fetchall()

    if geo_data:
        # Unpack data into lists
        countries, num_bookings = zip(*geo_data)

        # Create choropleth map using Plotly with lists
        fig = px.choropleth(
            dict(
                country=countries,
                num_bookings=num_bookings
            ),
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
        graph_html = "<p>No data available for countries.</p>"

    return HTMLResponse(content=graph_html)
