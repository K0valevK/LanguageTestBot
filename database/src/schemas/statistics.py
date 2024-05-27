from pydantic import BaseModel
from typing import Optional


class StatisticsBase(BaseModel):
    user_id: int


class StatisticsCreate(StatisticsBase):
    correct_answers: Optional[int]
    tasks_answered: Optional[int]
    max_unlimited_score: Optional[int]


class Statistics(StatisticsBase):
    id: int
    correct_answers: int
    tasks_answered: int
    max_unlimited_score: int

    class Config:
        from_attributes = True
