from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, TypeVar, Generic

from loguru import logger
from pydantic import Field

from common.config.config import MinioConfig
from common.config.constants import SOURCE_PATH
from common.minio import MinioClient

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]
Transaction = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{64}$")]

T = TypeVar("T")
minio_config = MinioConfig()


@dataclass
class BaseFile(ABC, Generic[T]):
    content: T
    name: str
    write_params: dict = field(default_factory=lambda: {"mode": "w", "encoding": "utf-8"})

    def __post_init__(self):
        if minio_config.enabled:
            self.minio = MinioClient(minio_config)
        else:
            self.minio = None

    def save_to_cloud(self, target: Path, content: str | bytes):
        if minio_config.enabled:
            self.minio.write(target, content)

    def save_to_filesystem(self, target: Path, content: str | bytes):
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open(**self.write_params) as out:
            out.write(content)

    def get_path(self, address: Address) -> Path:
        return SOURCE_PATH / address / self.name

    def get_content(self) -> str | bytes:
        return self.content

    def write(self, address: Address):
        content = self.get_content()
        target = self.get_path(address)
        self.save_to_filesystem(target, content)
        self.save_to_cloud(target, content)
        logger.info("[{}] Saved {}", address, target.name)
