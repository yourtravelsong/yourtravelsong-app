from pydantic_settings import BaseSettings

class Settings(BaseSettings, cli_parse_args=True, cli_exit_on_error=False):
    MISTRAL_API_KEY: str
    PINECONE_API_KEY: str
    VectorStoreName: str
    mongodb_name: str
    mongodb_collection_name: str

if __name__ == "__main__":
    settings = Settings()
