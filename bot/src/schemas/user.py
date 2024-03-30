from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    telegram_id: int


class UserCreate(UserBase):
    username: Optional[str]
    correct_answers: Optional[int]
    tasks_answered: Optional[int]
    max_unlimited_score: Optional[int]


class User(UserBase):
    id: int
    username: str
    correct_answers: int
    tasks_answered: int
    max_unlimited_score: int

    class Config:
        from_attributes = True
