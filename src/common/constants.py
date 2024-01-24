from pathlib import Path

from pydantic_settings import BaseSettings


class PathConfig(BaseSettings):
    base_path: Path = Path(".")


config = PathConfig()

SOURCE_PATH = config.base_path / "sources"
BYTECODE_PATH = config.base_path / "bytecode"
BYTECODE_FILE = BYTECODE_PATH / "bytecode.bin"
