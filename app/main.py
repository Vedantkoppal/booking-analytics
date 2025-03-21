from app.core.config import create_app
from fastapi.staticfiles import StaticFiles
from app.api.analytics import router as analytics_router
from app.api.revenue_api import router as revenue_router
from app.api.cancellation_api import router as cancellation_router



# Create FastAPI app
app = create_app()
# app.mount("/static", StaticFiles(directory="app/static"), name="static")
# Include routers
app.include_router(analytics_router)
app.include_router(revenue_router)
app.include_router(cancellation_router)

# from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
# import plotly.express as px
# import plotly.io as pio

# # Create FastAPI app
# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# def get_test_graph():
#     # ✅ Sample data for a quick graph
#     df = px.data.gapminder().query("country == 'India'")
    
#     # ✅ Create a simple line graph (GDP vs Year)
#     fig = px.line(df, x="year", y="gdpPercap", title="GDP Per Capita of India")

#     # ✅ Use plotly.io.to_html() to get only the graph's div
#     graph_html = pio.to_html(fig, full_html=False)

#     # ✅ Return graph inside a basic HTML template
#     html_content = f"""
#     <html>
#     <head>
#         <title>Plotly Test</title>
#     </head>
#     <body>
#         <h2>Plotly Graph Test</h2>
#         <div id="graph-container">
#             {graph_html}
#         </div>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)
