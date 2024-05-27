from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class Answer(Base):
    __tablename__ = 'answer'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    task_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    text: Mapped[str] = mapped_column(String)
    text_pos: Mapped[int] = mapped_column(Integer)
    is_true: Mapped[bool] = mapped_column(Boolean)
