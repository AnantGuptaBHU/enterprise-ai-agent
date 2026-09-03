from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    database_url: str
    # secret_key: str
    # algorithm: str
    # access_token_expire_minutes: int
    # max_retries: int
    # retry_delay: int
    # gemini_api_key: str
    # gemini_api_url: str
    # llm_timeout: int
    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8"
    # )

settings = Settings()