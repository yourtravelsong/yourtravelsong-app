from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGODB_CONNECTION_STRING: str

if __name__ == "__main__":
    settings = Config()