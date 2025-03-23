from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.core.llm_config import query_engine
from app.core.data_config import CHAT_HISTORY
import os
import json
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Path to store chat history
CHAT_HISTORY_FILE = CHAT_HISTORY

# Function to load existing chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []  # Return empty list if error or file not found
    return []

# Function to save updated chat history
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# ================================
# GET /ask - Load UI
# ================================
@router.get("/ask", response_class=HTMLResponse)
def get_ask_page(request: Request):
    return templates.TemplateResponse("ask.html", {"request": request})

# ================================
# POST /ask - Process Question and Get Answer
# ================================
@router.post("/ask")
async def process_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question")

        if not question:
            raise HTTPException(status_code=400, detail="No question provided")

        # Get answer from query engine
        response = query_engine.query(question)

        # Load existing history and append new entry
        chat_history = load_chat_history()
        chat_history.append({
            "question": question,
            "answer": str(response),
            "timestamp": datetime.now().isoformat()
        })

        # Save updated chat history
        save_chat_history(chat_history)

        # Return answer to UI
        return JSONResponse(content={"answer": str(response)})

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)
