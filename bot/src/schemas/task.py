from pydantic import BaseModel


class TaskBase(BaseModel):
    type: str
    text: str
    difficulty: float


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
