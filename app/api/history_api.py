from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.core.data_config import CHAT_HISTORY
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Path to query history JSON
HISTORY_FILE = CHAT_HISTORY

# ================================
# 1. GET /history - Load Query History Page
# ================================
@router.get("/history", response_class=HTMLResponse)
def get_history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})


# ================================
# 2. GET /get_query_history - Fetch Query History Data
# ================================
@router.get("/get_query_history")
def get_query_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history_data = json.load(file)
    else:
        history_data = []

    return JSONResponse(content={"history": history_data})
