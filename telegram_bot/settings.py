from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    tg_token: str = Field(default="token", alias="TG_BOT_TOKEN")
    get_proxy_url: str = Field(default="token", alias="PROXY_GET_URL")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
