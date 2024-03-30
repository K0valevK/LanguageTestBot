from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_task_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/task"
    database_statistic_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/statistic"
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    me_host: str = "0.0.0.0"
    me_port: int = 8000


settings = Settings()
