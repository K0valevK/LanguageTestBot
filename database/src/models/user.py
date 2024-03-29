from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    correct_answers: Mapped[int] = mapped_column(Integer)
    tasks_answered: Mapped[int] = mapped_column(Integer)
