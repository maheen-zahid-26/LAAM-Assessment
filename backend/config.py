from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

    cors_origin: str = "http://localhost:3000"

    low_stock_max: int = 3

    alternatives_price_tolerance: float = 0.20
    alternatives_limit: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
