# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from app.schemas.account import Account


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {"from_attributes": True}


class UserAccount(BaseModel):
    id: int
    email: str
    full_name: str
    accounts: list[Account] = []

    model_config = {"from_attributes": True}