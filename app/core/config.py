from typing import Any, List, Optional
from urllib.parse import quote_plus

from phonenumbers.phonenumberutil import PhoneNumberFormat
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_extra_types.phone_numbers import PhoneNumber
from pydantic_settings import BaseSettings, SettingsConfigDict

PhoneNumber.phone_format = "INTERNATIONAL"
PhoneNumber.default_region_code = "KR"



class Settings(BaseSettings):
    # FastAPI
    VERSION: str = "v1"
    API_V1_STR: str = "v1"
    PROJECT_NAME: str = "Simple FastAPI CRUD"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PHONE_FORMAT: int = PhoneNumberFormat.INTERNATIONAL

    # Database
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SCHEME: str
    POSTGRES_ECHO: bool = False
    EXPIRE_ON_COMMIT: bool = False

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    ENV: str = "production"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")  # noqa
    @classmethod
    def assemble_db_connection(cls, v: str | None, info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=info.data.get("POSTGRES_SCHEME"),
            username=info.data.get("POSTGRES_USER"),
            password=quote_plus(info.data.get("POSTGRES_PASSWORD")),
            host=info.data.get("POSTGRES_HOST"),
            port=int(info.data.get("POSTGRES_PORT")),
            path=info.data.get("POSTGRES_DATABASE", ""),
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
