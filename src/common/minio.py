from io import BytesIO
from pathlib import Path

from loguru import logger
from minio import Minio

from common.config.config import MinioConfig
from common.config.constants import SOURCE_PATH


class MinioClient:
    """
    The `MinioClient` class is a Python class that provides methods for writing data to a MinIO object
    storage server.
    """

    def __init__(self):
        self.config = MinioConfig()
        if self.config.enabled:
            self.client = Minio(
                self.config.endpoint,
                access_key=self.config.access_key,
                secret_key=self.config.secret_key,
                secure=self.config.secure,
            )

    def prepare_name(self, target: Path) -> str:
        """
        The function `prepare_name` takes a target path and returns a modified version of the path by
        removing a prefix.

        :param target: The `target` parameter is of type `Path`, which is a class representing a file or
        directory path. It is the path that you want to prepare the name for
        :type target: Path
        :return: a string.
        """
        prefix = str(SOURCE_PATH)
        return str(target).replace(prefix, "")

    def prepare_data(self, content: str | bytes) -> tuple[BytesIO, int]:
        """
        The function "prepare_data" takes in a string or bytes content, converts it to a BytesIO object,
        and returns the BytesIO object along with the number of bytes in the content.

        :param content: The `content` parameter can be either a string (`str`) or bytes (`bytes`)
        :type content: str | bytes
        :return: a tuple containing two elements. The first element is a BytesIO object, which is a
        binary stream that can be used to read or write bytes. The second element is an integer
        representing the number of bytes in the binary stream.
        """
        if isinstance(content, str):
            binary = BytesIO(content.encode())
        else:
            binary = BytesIO(content)
        return binary, binary.getbuffer().nbytes

    def write(self, target: Path, content: str | bytes):
        """
        The function writes content to a specified target path using an AWS S3 client.

        :param target: The `target` parameter is of type `Path`, which represents a file or directory
        path. It is the location where the content will be written to
        :type target: Path
        :param content: The `content` parameter can be either a string (`str`) or bytes (`bytes`). It
        represents the data that you want to write to the target file
        :type content: str | bytes
        :return: If the `self.config.enabled` condition is not met, then `None` is being returned.
        """
        if not self.config.enabled:
            return
        try:
            name = self.prepare_name(target)
            data, length = self.prepare_data(content)
            self.client.put_object(self.config.bucket_name, name, data, length)
        except Exception as exc:
            logger.warning(exc)
