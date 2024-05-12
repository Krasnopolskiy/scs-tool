from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Generic, TypeVar

from loguru import logger
from pydantic import Field

from common.constants import SOURCE_PATH
from common.minio import get_minio_client, minio_config

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]
Transaction = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{64}$")]

T = TypeVar("T")


@dataclass
class BaseFile(ABC, Generic[T]):
    content: T
    name: str
    write_params: dict = field(default_factory=lambda: {"mode": "w", "encoding": "utf-8"})

    def __post_init__(self):
        if minio_config.enabled:
            self.minio = get_minio_client()
        else:
            self.minio = None

    def save_to_cloud(self, target: Path, content: str | bytes):
        """
        The function `save_to_cloud` writes content to a specified target path in a cloud storage
        service using Minio if the Minio configuration is enabled.

        :param target: The `target` parameter in the `save_to_cloud` method is expected to be a Path
        object, which represents the location where the content will be saved in the cloud storage
        :type target: Path
        :param content: The `content` parameter in the `save_to_cloud` method can be either a string
        (`str`) or bytes (`bytes`) type. This parameter represents the data that you want to save to the
        cloud storage using the `minio.write` method. You can pass either a string or bytes object
        :type content: str | bytes
        """
        if minio_config.enabled:
            self.minio.write(target, content)

    def save_to_filesystem(self, target: Path, content: str | bytes):
        """
        The function `save_to_filesystem` saves content to a file in the filesystem at the specified
        target path.

        :param target: The `target` parameter in the `save_to_filesystem` function is expected to be a
        `Path` object representing the location where the content will be saved in the filesystem. The
        function creates the necessary directories leading up to the target path if they do not already
        exist
        :type target: Path
        :param content: The `content` parameter in the `save_to_filesystem` method can accept either a
        string (`str`) or bytes (`bytes`) data type. This means you can pass either a text-based content
        (string) or binary data (bytes) to be saved to the filesystem
        :type content: str | bytes
        """
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open(**self.write_params) as out:
            out.write(content)

    def get_path(self, address: Address) -> Path:
        """
        The function `get_path` returns a `Path` object by concatenating `SOURCE_PATH`, an `Address`,
        and the name of the object.

        :param address: The `address` parameter in the `get_path` method is of type `Address`. It is
        used to specify the address that will be part of the path returned by the method
        :type address: Address
        :return: A Path object representing the path to a specific address based on the SOURCE_PATH and
        the name of the object.
        """
        return SOURCE_PATH / address / self.name

    def get_content(self) -> str | bytes:
        """
        This function named `get_content` returns the content stored in the object it is called on,
        which can be either a string or bytes.
        :return: The `get_content` method is returning the `content` attribute of the object. The return
        type can be either a string or bytes, as indicated by the type hint `str | bytes`.
        """
        return self.content

    def write(self, address: Address):
        """
        The `write` function saves content to both the filesystem and cloud storage, logging the action.

        :param address: The `address` parameter in the `write` method is an instance of the `Address`
        class. It is used to specify the location where the content will be written to, both in the
        local filesystem and in the cloud storage
        :type address: Address
        """
        content = self.get_content()
        target = self.get_path(address)
        self.save_to_filesystem(target, content)
        self.save_to_cloud(target, content)
        logger.info("[{}] Saved {}", address, target.name)
