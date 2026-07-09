import time
import logging

from fastapi import APIRouter, HTTPException, Query

from ai.models.schemas import ChatRequest, ChatResponse
from app.dependencies import get_graph

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "healthy", "service": "smart-restaurant-assistant"}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=422, detail="Message cannot be empty")

    start_time = time.time()
    logger.info(f"Chat request | thread_id={request.thread_id}")

    try:
        graph = get_graph()
        result = await graph.ainvoke(
            {
                "user_query": request.message,
                "thread_id": request.thread_id,
                "conversation_history": [],
            },
            {"configurable": {"thread_id": request.thread_id}},
        )

        execution_time = time.time() - start_time
        logger.info(f"Chat completed | time={execution_time:.2f}s")

        return ChatResponse(
            response=result.get("final_response", ""),
            sources=result.get("sources", []),
            tool_calls=result.get("tool_calls", []),
            confidence=result.get("confidence", 0.0),
            execution_time=round(execution_time, 2),
        )
    except Exception as e:
        logger.error(f"Chat failed | thread_id={request.thread_id} | error={e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset(thread_id: str = Query(..., description="Thread ID to reset")):
    try:
        logger.info(f"Memory reset | thread_id={thread_id}")
        return {"status": "ok", "message": "Conversation memory cleared"}
    except Exception as e:
        logger.error(f"Reset failed | thread_id={thread_id} | error={e}")
        raise HTTPException(status_code=500, detail=str(e))
