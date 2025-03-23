from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from app.core.data_config import get_db, DB_PATH, CHAT_HISTORY, GROUPED_DATA
from sqlalchemy import text
from app.core.llm_config import query_engine
import os
import json

# Create router
router = APIRouter()

# Required files in app/data
REQUIRED_FILES = [
    CHAT_HISTORY,
    GROUPED_DATA,
    DB_PATH,  # DB Path from config
]


### ============================
### API: /health - Check System Status
### ============================
@router.get("/health")
async def health_check(request: Request):
    health_report = {
        "server_status": "running",
        "db_status": "pending",
        "llm_status": "pending",
        "data_files_status": "pending",
        "api_routes_status": "pending",
    }

    try:
        # ✅ Check DB Connection
        db = next(get_db())
        db.execute(text("SELECT 1"))
        db.close()
        health_report["db_status"] = "ok"
    except Exception as e:
        health_report["db_status"] = f"error: {str(e)}"


#  Due to slow processing of CPU and limited memory, i have commented below code 
#  Feel free to uncomment when you have enough resources    
    # try:
    #     # ✅ Check LLM Connection
    #     test_query = "Test connection"
    #     response = query_engine.query(test_query)
    #     if response:
    #         health_report["llm_status"] = "ok"
    #     else:
    #         health_report["llm_status"] = "error: No response"
    # except Exception as e:
    #     health_report["llm_status"] = f"error: {str(e)}"
    # 


    # ✅ Check Required Files
    missing_files = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing_files.append(file)

    if not missing_files:
        health_report["data_files_status"] = "ok"
    else:
        health_report["data_files_status"] = f"Missing files: {', '.join(missing_files)}"

    try:
        # ✅ Check API Routes (Get router from request instead of app)
        route_list = []
        for route in request.app.router.routes:
            if hasattr(route, "path"):
                route_list.append(route.path)

        health_report["api_routes_status"] = {"available_routes": route_list}
    except Exception as e:
        health_report["api_routes_status"] = f"error: {str(e)}"

    # ✅ Return Health Report
    return JSONResponse(content=health_report)
