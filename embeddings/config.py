from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HUGGINGFACE_API_KEY: str
    OPENAI_API_KEY: str
    MISTRAL_API_KEY: str
    PINECONE_API_KEY: str

settings = Settings()