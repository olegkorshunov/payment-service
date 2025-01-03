from typing import ClassVar

import pika
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitSettings(BaseSettings):
    host: str = "rabbitmq"
    port: int = 5672
    credentials: ClassVar = pika.PlainCredentials("guest", "guest")
    queue_name: str = "test-queue"
    exchange_name: str = "example_exchange"
    exchange_type: str = "fanout"

    model_config = SettingsConfigDict(env_prefix="rabbit_")
