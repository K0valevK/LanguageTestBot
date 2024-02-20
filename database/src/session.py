from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from generic_repository import GenericRepository


DATABASE_URL = "postgresql+asyncpg://language_bot:language_bot@localhost/task_database"


engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
repository = GenericRepository(engine)
