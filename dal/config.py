from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGODB_CONNETCTION_STRING: str
    PORT: int

settings = Config()