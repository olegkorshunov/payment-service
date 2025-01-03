from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = "Payments service"
    version: str = "2023.1"
    docs_url: str = "/docs"
    root_path: str = ""
    debug: bool = False

    log_level: str = "DEBUG"
    log_filter_urls: list[str] = ["/api/v1/ping", "/docs", "/openapi.json", "/metrics"]

    model_config = SettingsConfigDict(env_prefix="app_")
