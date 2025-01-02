from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    password: str = "1234"

    class Config:
        env_prefix = "redis_"
        env_file = ".env"
