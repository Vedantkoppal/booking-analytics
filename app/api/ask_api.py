from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.llm_config import query_engine

router = APIRouter()


# Request model
class AskRequest(BaseModel):
    question: str


# Route for /ask endpoint
@router.post("/ask")
async def ask_question(request: AskRequest):
    try:
        # Get user question
        question = request.question.strip()

        # Validate empty input
        if not question:
            return {"answer": "Please ask a valid question."}

        # Query LLM and get response
        response = query_engine.query(question)

        # Extract answer from response
        answer = str(response) if response else "Sorry, I couldn't find an answer."

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")
