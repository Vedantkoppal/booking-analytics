from app.core.config import create_app
from app.api.analytics import router as analytics_router
from app.api.revenue_api import router as revenue_router
from app.api.cancellation_api import router as cancellation_router
from app.api.geo_distribution_api import router as geo_distribution_router
from app.api.lead_time_api import router as lead_time_router
from app.api.ask_api import router as ask_router
from app.api import health_api
from app.api import history_api







# Create FastAPI app
app = create_app()

import plotly.io as pio
pio.templates.default = None

app.include_router(analytics_router)
app.include_router(revenue_router)
app.include_router(cancellation_router)
app.include_router(geo_distribution_router)
app.include_router(lead_time_router)
app.include_router(ask_router)
app.include_router(health_api.router)
app.include_router(history_api.router)