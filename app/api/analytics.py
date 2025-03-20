from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.config import templates

router = APIRouter()

@router.get("/analytics", response_class=HTMLResponse)
def show_base_template(request: Request):
    # Render base.html for testing
    return templates.TemplateResponse("analytics.html", {"request": request})
