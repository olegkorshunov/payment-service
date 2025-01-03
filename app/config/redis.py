from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    password: str = "1234"

    model_config = SettingsConfigDict(env_prefix="redis_")
