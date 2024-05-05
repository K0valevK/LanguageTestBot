from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str] = mapped_column(String)
