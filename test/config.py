from pydantic_settings import BaseSettings

class TestArguments(BaseSettings):
    env_file: str = "../index.env"
    log_level: str = "DEBUG"