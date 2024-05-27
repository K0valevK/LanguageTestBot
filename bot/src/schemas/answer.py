from pydantic import BaseModel


class AnswerBase(BaseModel):
    task_id: int
    text: str
    text_pos: int
    is_true: bool


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int

    class Config:
        from_attributes = True
