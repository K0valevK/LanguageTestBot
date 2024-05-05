from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    telegram_id: int


class UserCreate(UserBase):
    username: Optional[str]


class User(UserBase):
    id: int
    username: str

    class Config:
        from_attributes = True
