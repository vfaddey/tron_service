from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    DB_URL: str


    class Config:
        env_file = '.env'



settings = Settings()