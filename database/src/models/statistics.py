from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class Statistics(Base):
    __tablename__ = 'statistics'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    correct_answers: Mapped[int] = mapped_column(Integer)
    tasks_answered: Mapped[int] = mapped_column(Integer)
    max_unlimited_score: Mapped[int] = mapped_column(Integer)
