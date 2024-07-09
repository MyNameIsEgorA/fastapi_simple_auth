from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    MODE: Literal["DEV", "TEST", "PROD"]

    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int

    TEST_DB_HOST: str
    TEST_DB_NAME: str
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_PORT: int

    SECRET_KEY: str
    ALGORITHM: str

    def get_database_url(self) -> str:
        if self.MODE == "DEV":
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        if self.MODE == "TEST":
            return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    class Config:
        env_file = '.env'


settings = Settings()
