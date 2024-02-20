from pydantic import BaseModel
from enum import Enum


class TaskDtoBase(BaseModel):
    type: Enum
    text: str
    difficulty: float


class TaskDtoCreate(TaskDtoBase):
    pass


class TaskDto(TaskDtoBase):
    id: int

    class Config:
        orm_mode = True
