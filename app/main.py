
"""
Application entry point.

This module:
- Wires together all RAG components
- Exposes a FastAPI endpoint for chatbot interaction
- Ensures strict CSV-only answering
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from data.loader import DataLoader
from app.executor import RetrievalEngine
from app.context_builder import RAGContextBuilder, EmptyContextError
from app.intent_parser import IntentParser, IntentParsingError
from app.validator import Validator, ValidationError
from app.formatter import AnswerFormatter


# -----------------------------
# FastAPI App Initialization
# -----------------------------

app = FastAPI(
    title="Fund RAG Chatbot",
    description="A CSV-grounded RAG chatbot for fund analytics",
    version="1.0.0"
)


# -----------------------------
# Load Data ONCE at Startup
# -----------------------------

data_loader = DataLoader(data_dir="data")
data_loader.load()

retrieval_engine = RetrievalEngine(data_loader)
intent_parser = IntentParser()
answer_formatter = AnswerFormatter()


# -----------------------------
# API Request / Response Models
# -----------------------------

class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# -----------------------------
# Root and Health Endpoints
# -----------------------------

@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Fund RAG Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Send a question to the chatbot",
            "GET /docs": "Interactive API documentation",
            "GET /health": "Health check endpoint"
        }
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "data_loaded": data_loader._holdings_df is not None and data_loader._trades_df is not None
    }


# -----------------------------
# Chat Endpoint
# -----------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        # 1. Parse intent using LLM
        intent = intent_parser.parse(request.question)
        Validator.validate_intent(intent)

        # 2. Execute retrieval based on intent
        intent_type = intent.get("intent")
        entity = intent.get("entity")
        metric = intent.get("metric")

        if intent_type == "COUNT" and metric == "holdings_count":
            count = retrieval_engine.count_holdings(entity)
            context = RAGContextBuilder.build_count_context(
                entity_type="fund",
                entity_name=entity,
                count=count,
                source="holdings.csv"
            )

        elif intent_type == "COUNT" and metric == "trades_count":
            count = retrieval_engine.count_trades(entity)
            context = RAGContextBuilder.build_count_context(
                entity_type="fund",
                entity_name=entity,
                count=count,
                source="trades.csv"
            )

        elif intent_type == "AGGREGATE" and metric == "PL_YTD":
            value = retrieval_engine.aggregate_pl_ytd(entity)
            context = RAGContextBuilder.build_aggregate_context(
                entity_type="fund",
                entity_name=entity,
                metric="PL_YTD",
                value=value,
                source="holdings.csv"
            )

        elif intent_type == "COMPARE" and metric == "PL_YTD":
            result = retrieval_engine.best_performing_fund_ytd()
            context = RAGContextBuilder.build_comparison_context(
                metric="PL_YTD",
                best_entity=result["fund"],
                best_value=result["pl_ytd"],
                source="holdings.csv"
            )

        else:
            context = RAGContextBuilder.build_empty_context(
                reason="Unsupported or incomplete query."
            )

        # 3. Validate context
        Validator.validate_context(context)

        # 4. Generate final answer using LLM
        answer = answer_formatter.format(context)

        return ChatResponse(answer=answer)

    except (
        IntentParsingError,
        ValidationError,
        EmptyContextError,
        Exception
    ):
        return ChatResponse(answer="Sorry can not find the answer")


from fastapi.responses import HTMLResponse
from pathlib import Path

@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    ui_path = Path("ui/index.html")
    return ui_path.read_text(encoding="utf-8")
