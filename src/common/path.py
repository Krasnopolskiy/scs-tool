from pathlib import Path

from pydantic_settings import BaseSettings


class PathConfig(BaseSettings):
    base_path: Path = Path(".")


path_config = PathConfig()
