"""
FastAPI Backend Server
Bridges the Streamlit frontend to the LangGraph agent pipeline.
"""

import sys
import os

# Add backend directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from app import run_query, setup_database, get_database_schema
from chart_engine import recommend_chart

# Load environment variables
load_dotenv()

# --- FastAPI App ---
api = FastAPI(
    title="SQL Insights Generator API",
    description="Agentic SQL analysis pipeline powered by LangGraph + Gemini",
    version="1.0.0"
)

# CORS for local development
api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory chat history (per session, resets on restart)
chat_memory = []


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    question: str
    plan: str
    sql_query: str
    columns: list
    data: list
    analysis: str
    insights: str
    retries: int
    error: Optional[str]
    chart_recommendation: dict


# --- Startup Event ---
@api.on_event("startup")
def startup_event():
    """Initialize the database with seed data on startup."""
    print("🚀 Initializing database with seed data...")
    db_conn = setup_database()
    schema = get_database_schema(db_conn)
    db_conn.close()
    print(f"✅ Database ready. Schema loaded ({len(schema)} chars)")


# --- Endpoints ---
@api.get("/health")
def health_check():
    return {"status": "healthy", "service": "SQL Insights Generator API"}


@api.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    """
    Process a natural language business question through the full agent pipeline.
    Returns structured results including chart recommendation.
    """
    global chat_memory

    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    try:
        print(f"\n{'='*60}")
        print(f"📥 New Query: {request.question}")
        print(f"{'='*60}")

        # Run the full LangGraph pipeline
        result = run_query(
            question=request.question,
            chat_history=chat_memory
        )

        # Generate chart recommendation
        chart_rec = recommend_chart(
            columns=result.get("columns", []),
            data=result.get("data", []),
            question=request.question
        )

        # Update chat memory for follow-up context
        chat_memory.append({"role": "user", "content": request.question})
        chat_memory.append({"role": "assistant", "content": result.get("insights", "")})

        # Keep memory manageable (last 20 messages)
        if len(chat_memory) > 20:
            chat_memory = chat_memory[-20:]

        return QueryResponse(
            question=result["question"],
            plan=result["plan"],
            sql_query=result["sql_query"],
            columns=result["columns"],
            data=result["data"],
            analysis=result["analysis"],
            insights=result["insights"],
            retries=result["retries"],
            error=result["error"],
            chart_recommendation=chart_rec
        )

    except Exception as e:
        print(f"❌ Error processing query: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


@api.post("/reset")
def reset_memory():
    """Reset the conversation memory."""
    global chat_memory
    chat_memory = []
    return {"status": "memory_cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:api", host="0.0.0.0", port=8000, reload=True)
