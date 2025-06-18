from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from ..core.settings import get_settings
from ..core.roles import get_allowed_departments
from ..schemas.login import TokenData, UserLogin, Token

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user database - this should be replaced with actual database
users_db = {
    "Tony": {"password": pwd_context.hash("password123"), "role": "engineering"},
    "Bruce": {"password": pwd_context.hash("securepass"), "role": "marketing"},
    "Sam": {"password": pwd_context.hash("financepass"), "role": "finance"},
    "Peter": {"password": pwd_context.hash("pete123"), "role": "engineering"},
    "Sid": {"password": pwd_context.hash("sidpass123"), "role": "marketing"},
    "Natasha": {"password": pwd_context.hash("hrpass123"), "role": "hr"}
}

async def authenticate_user(username: str, password: str) -> Optional[dict]:
    user = users_db.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return {"username": username, "role": user["role"]}

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({ "exp": expire, "sub": data["sub"], "role": data["role"] })
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = users_db.get(token_data.username)
    if user is None:
        raise credentials_exception
    return {"username": token_data.username, "role": user["role"]}



async def login(login_data: UserLogin) -> Token:
    user = await authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return Token(access_token=access_token, token_type="bearer")
