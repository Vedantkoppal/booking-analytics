from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
import sqlite3

def create_app() -> FastAPI:
    app = FastAPI(
        title="Booking Analytics API",
        description="API to generate interactive booking analytics with Plotly and FastAPI.",
        version="1.0.0",
    )
    return app

# template engine
templates = Jinja2Templates(directory="app/templates")


