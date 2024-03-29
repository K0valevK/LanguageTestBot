from pydantic import BaseModel


class UserBase(BaseModel):
    telegram_id: int
    correct_answers: int
    tasks_answered: int


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
