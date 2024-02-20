from pydantic import BaseModel


class AnswerDtoBase(BaseModel):
    text: str
    text_pos: int
    is_true: bool


class AnswerDtoCreate(AnswerDtoBase):
    pass


class AnswerDto(AnswerDtoBase):
    id: int
    task_id: int

    class Config:
        orm_mode = True
