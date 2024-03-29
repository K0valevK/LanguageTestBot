from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = "6507913188:AAHx-QFkh87DrHqjcU27RzJnzPKdBdgFgMw"
    database_host: str = "localhost"
    database_port: int = 8000


settings = Settings()
