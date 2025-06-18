from pydantic import BaseModel, EmailStr
from typing import Union, Optional
from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str 