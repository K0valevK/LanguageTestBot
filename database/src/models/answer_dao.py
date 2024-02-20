from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from database.src.session import Base


class AnswerDao(Base):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer)
    text: Mapped[str] = mapped_column(String)
    text_pos: Mapped[int] = mapped_column(Integer)
    is_true: Mapped[bool] = mapped_column(Boolean)
