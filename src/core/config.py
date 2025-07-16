from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import  BaseSettings, SettingsConfigDict
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
class DataBaseConfig(BaseModel):
    url: PostgresDsn
    test_url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
class RunConfig(BaseModel):
    host:str = "0.0.0.0"
    port:int = 8000
    debug:int = 1


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=str(env_path)
        )
    db: DataBaseConfig
    run:RunConfig = RunConfig()

settings = Settings()



