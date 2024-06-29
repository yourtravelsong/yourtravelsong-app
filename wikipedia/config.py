from pydantic_settings import BaseSettings


class Email(BaseSettings):
    EMAIL: str


settings = Email()