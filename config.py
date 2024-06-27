import os
from typing import Union

from pydantic_settings import BaseSettings


class Base(BaseSettings):
    API_V1_STR: str = "/v1"
    SESSION_TOKEN_EXPIRE_SECONDS: int = 43200
    NUM_DATAFLOW_PREVIEW_ROWS: int = 100

    TAVILY_API_KEY: str

    GOOGLE_API_KEY: str

    YI_API_KEY: str
    YI_BASE_URL: str

    GROQ_API_KEY: str
    GROQ_BASE_URL: str

    class Config:
        case_sensitive = True


class Dev(Base):
    class Config:
        env_file = ".env"
        case_sensitive = True


class Prod(Base):
    class Config:
        env_file = "prod.env"
        case_sensitive = True


config = dict(dev=Dev, prod=Prod)
settings: Union[Dev, Prod] = config[os.environ.get("ENV", "dev").lower()]()
