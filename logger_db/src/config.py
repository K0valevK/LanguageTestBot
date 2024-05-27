from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = "My FastAPI project"
    me_host: str = "localhost"
    me_port: int = 8003
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    kafka_topic_uj: str = "user_journey"
    kafka_topic_errors: str = "errors"
    ch_host: str = "localhost"
    ch_port: int = 9000


settings = Settings()
