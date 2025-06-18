from typing import Dict
<<<<<<< HEAD
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
=======

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

# Dummy user database
users_db: Dict[str, Dict[str, str]] = {
    "Tony": {"password": "password123", "role": "engineering"},
    "Bruce": {"password": "securepass", "role": "marketing"},
    "Sam": {"password": "financepass", "role": "finance"},
    "Peter": {"password": "pete123", "role": "engineering"},
    "Sid": {"password": "sidpass123", "role": "marketing"},
    "Natasha": {"passwoed": "hrpass123", "role": "hr"}
}


# Authentication dependency
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    password = credentials.password
    user = users_db.get(username)
    if not user or user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"username": username, "role": user["role"]}


# Login endpoint
@app.get("/login")
def login(user=Depends(authenticate)):
    return {"message": f"Welcome {user['username']}!", "role": user["role"]}


# Protected test endpoint
@app.get("/test")
def test(user=Depends(authenticate)):
    return {"message": f"Hello {user['username']}! You can now chat.", "role": user["role"]}


# Protected chat endpoint
@app.post("/chat")
def query(user=Depends(authenticate), message: str = "Hello"):
    return "Implement this endpoint."
>>>>>>> 29f306d6af5bcaf63c638cfd56074b4bebc1b5d4
