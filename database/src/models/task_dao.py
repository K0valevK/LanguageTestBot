from typing import Literal
from typing import get_args
from sqlalchemy import Integer, String, Double, Enum
from sqlalchemy.orm import mapped_column, Mapped
from database.src.session import Base

Task_type = Literal['paronym', 'accent']


class TaskDao(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    type: Mapped[Task_type] = mapped_column(Enum(*get_args(Task_type), name='type'))
    text: Mapped[str] = mapped_column(String)
    difficulty: Mapped[float] = mapped_column(Double)
