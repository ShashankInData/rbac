from typing import Dict
import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, chat
from app.core.settings import get_settings
from app.services.auth_service import get_current_user

settings = get_settings()

# Create necessary directories
os.makedirs(settings.CHROMA_PERSIST_DIRECTORY, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Internal Chatbot with Role Based Access Control",
    version="0.1.0"
)

# Include routers before CORS
app.include_router(auth.router)
app.include_router(chat.router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protected test endpoint
@app.get("/test")
async def test(user=Depends(get_current_user)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}

# Protected chat endpoint
@app.post("/chat")
async def query(user=Depends(get_current_user), message: str = "Hello"):
    return "Implement this endpoint."

@app.get("/")
async def root():
    return {"message": "Welcome to RBAC Chatbot API"}

@app.get("/_debug/settings")
def _debug_settings():
    # dump whatever Settings() has loaded from .env
    return get_settings().dict()
