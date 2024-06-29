from pydantic_settings import BaseSettings

class HuggingFaceSettings(BaseSettings):
    HUGGINGFACE_API_KEY: str