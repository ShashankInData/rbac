from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime = datetime.now()

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[str]] = None

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None 