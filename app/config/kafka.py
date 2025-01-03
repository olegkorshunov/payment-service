from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str] = ["kafka:9092"]
    topic: str = "test-topic"

    model_config = SettingsConfigDict(env_prefix="kafka_")
