from io import BytesIO
from pathlib import Path

from loguru import logger
from minio import Minio

from common.config.config import MinioConfig
from common.config.constants import SOURCE_PATH


def prepare_name(target: Path) -> str:
    prefix = str(SOURCE_PATH)
    return str(target).replace(prefix, "")


def prepare_data(content: str | bytes) -> tuple[BytesIO, int]:
    if isinstance(content, str):
        binary = BytesIO(content.encode())
    else:
        binary = BytesIO(content)
    return binary, binary.getbuffer().nbytes


class MinioClient:
    """
    The `MinioClient` class is a Python class that provides methods for writing data to a MinIO object
    storage server.
    """

    def __init__(self, config: MinioConfig):
        self.bucket_name = config.bucket_name
        self.client = Minio(
            config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.secure,
        )

    def write(self, target: Path, content: str | bytes):
        try:
            name = prepare_name(target)
            data, length = prepare_data(content)
            self.client.put_object(self.bucket_name, name, data, length)
        except Exception as exc:
            logger.warning(exc)
