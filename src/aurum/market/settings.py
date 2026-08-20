from pydantic_settings import BaseSettings, SettingsConfigDict


class MT5Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    mt5_login: int
    mt5_password: str
    mt5_server: str
