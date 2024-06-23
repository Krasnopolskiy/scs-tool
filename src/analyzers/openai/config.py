from pydantic import Field
from pydantic_settings import BaseSettings

CONFIG_PATH = "prompts"


class OpenAIConfig(BaseSettings):
    key: str = Field(default="", alias="OPENAI_API_KEY")
    model: str = Field(default="gpt-3.5-turbo", alias="OPENAI_MODEL")


openai_config = OpenAIConfig()
