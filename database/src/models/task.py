from sqlalchemy import Integer, String, Double
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String)
    difficulty: Mapped[float] = mapped_column(Double, index=True)
