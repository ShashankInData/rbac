from fastapi import APIRouter, Depends, HTTPException
from ..services.auth_service import get_current_user
from ..services.rag_service import RAGService
from ..schemas.chat import ChatRequest, ChatResponse
from ..core.settings import get_settings
from fastapi import HTTPException

settings = get_settings()
router = APIRouter(prefix=f"{settings.API_V1_STR}/chat", tags=["chat"])
rag_service = RAGService()

@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest, user=Depends(get_current_user)):
    try:
        return await rag_service.answer(request, user["role"])
    except Exception as e:
        # return the real error in JSON
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")