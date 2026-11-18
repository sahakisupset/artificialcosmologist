from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ads_api_token: str | None = None
    deepseek_api_key: str | None = None
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-reasoner"
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection: str = "cosmology-literature"
    ssl_ca_bundle: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
