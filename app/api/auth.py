from fastapi import APIRouter, Depends, HTTPException
from ..services import auth_service as auth_srv
from ..schemas.login import UserLogin, Token
from ..core.settings import get_settings

settings = get_settings()
router = APIRouter(prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login_endpoint(login_data: UserLogin):
    try:
        return await auth_srv.login(login_data)
    except Exception as e:
        # expose the real error in the response
        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {e}"
        )
