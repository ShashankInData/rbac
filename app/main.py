from fastapi import FastAPI, HTTPException
from .core.settings import get_settings
from .api import auth, chat
from fastapi.responses import JSONResponse

# Load settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Health check endpoint
@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

# Include API routers
app.include_router(auth.router)
app.include_router(chat.router)

# Exception handler for HTTP exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

