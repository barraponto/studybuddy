from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict()

    groq_model: str = Field(default="groq:llama-3.1-8b-instant")
    groq_api_key: str = Field(default="")
