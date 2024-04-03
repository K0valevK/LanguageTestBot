from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_version: str = "1.0"

    bot_token: str = "6507913188:AAHx-QFkh87DrHqjcU27RzJnzPKdBdgFgMw"
    database_host: str = "localhost"
    database_port: int = 8000
    kafka_host: str = "localhost"
    kafka_port: int = 9092
    topic_user: str = "user_journey"
    topic_error: str = "errors"


settings = Settings()
