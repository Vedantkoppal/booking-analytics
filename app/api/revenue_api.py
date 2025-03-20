from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.analytics_service import (
    generate_yearly_graph,
    generate_monthly_graph,
    generate_granular_graph,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/get_revenue_graph", response_class=HTMLResponse)
def get_revenue_graph(
    request: Request,
    trend_type: str = Query("yearly"),
    year: int = Query(None),
    month: str = Query(None),
    granularity: str = Query(None),
):
    # Validate input
    if not year:
        return HTMLResponse("<p>Please select a year.</p>")

    # Show monthly trend after selecting a year
    if trend_type == "monthly_trend":
        graph_html = generate_monthly_graph(year)

    elif trend_type in ["daily", "weekly"]:
        if not month:
            return HTMLResponse("<p>Please select a month.</p>")
        graph_html = generate_granular_graph(year, month, trend_type)

    else:
        graph_html = "<p>Invalid trend type selected.</p>"
    return HTMLResponse(graph_html)
# def get_revenue_graph(
#     trend_type: str = Query("yearly"),
#     year: int = Query(None),
#     month: str = Query(None),
#     granularity: str = Query(None),
# ):
#     if not year:
#         return JSONResponse({"error": "Please select a year."}, status_code=400)

#     if trend_type in ["daily", "weekly"]:
#         if not month:
#             return JSONResponse({"error": "Please select a month."}, status_code=400)
#         graph_data = generate_granular_graph(year, month, trend_type)
#     else:
#         return JSONResponse({"error": "Invalid trend type selected."}, status_code=400)

#     return JSONResponse(graph_data)

