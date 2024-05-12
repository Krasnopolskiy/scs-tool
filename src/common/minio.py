from io import BytesIO
from pathlib import Path

from loguru import logger
from minio import Minio
from pydantic import Field
from pydantic_settings import BaseSettings

from common.constants import SOURCE_PATH


def prepare_name(target: Path) -> str:
    """
    The function `prepare_name` takes a target path and returns a string with the prefix removed.

    :param target: The `target` parameter in the `prepare_name` function is expected to be a `Path`
    object representing the path to a file or directory
    :type target: Path
    :return: The function `prepare_name` takes a `Path` object as input and returns a string. It first
    converts the `SOURCE_PATH` to a string and assigns it to the variable `prefix`. Then, it replaces
    the `prefix` in the string representation of the `target` path with an empty string. Finally, it
    returns the modified string representation of the `target` path.
    """
    prefix = str(SOURCE_PATH)
    return str(target).replace(prefix, "")


def prepare_data(content: str | bytes) -> tuple[BytesIO, int]:
    """
    The function `prepare_data` takes a string or bytes input, converts it to a BytesIO object, and
    returns the BytesIO object along with the size of the data in bytes.

    :param content: The `content` parameter in the `prepare_data` function can be either a string
    (`str`) or bytes (`bytes`)
    :type content: str | bytes
    :return: The function `prepare_data` is returning a tuple containing two elements:
    1. The `BytesIO` object `binary` which contains the content in binary format.
    2. The size of the content in bytes, calculated using `binary.getbuffer().nbytes`.
    """
    if isinstance(content, str):
        binary = BytesIO(content.encode())
    else:
        binary = BytesIO(content)
    return binary, binary.getbuffer().nbytes


class MinioConfig(BaseSettings):
    enabled: bool = Field(alias="S3_ENABLED", default=False)
    host: str | None = Field(alias="MINIO_HOST", default=None)
    bucket_name: str | None = Field(alias="MINIO_BUCKET_NAME", default=None)
    access_key: str | None = Field(alias="MINIO_ROOT_USER", default=None)
    secret_key: str | None = Field(alias="MINIO_ROOT_PASSWORD", default=None)
    secure: bool | None = Field(alias="MINIO_SECURE", default=None)

    @property
    def endpoint(self) -> str:
        """
        The function returns the endpoint URL by combining the host and port number.
        :return: The endpoint URL in the format "{host}:9000".
        """
        return f"{self.host}:9000"


class MinioClient:
    def __init__(self, config: MinioConfig):
        self.bucket_name = config.bucket_name
        self.client = Minio(
            config.endpoint,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=config.secure,
        )

    def write(self, target: Path, content: str | bytes):
        """
        This function writes content to a specified target using an object storage client, handling
        exceptions and logging warnings.

        :param target: The `target` parameter in the `write` method is expected to be a `Path` object,
        which represents a file path where the content will be written to
        :type target: Path
        :param content: The `content` parameter in the `write` method can accept either a string (`str`)
        or bytes (`bytes`) type. This parameter represents the content that will be written to the
        specified `target` file
        :type content: str | bytes
        """
        try:
            name = prepare_name(target)
            data, length = prepare_data(content)
            self.client.put_object(self.bucket_name, name, data, length)
        except Exception as exc:
            logger.warning(exc)


minio_config = MinioConfig()


def get_minio_client() -> MinioClient:
    """
    The function `get_minio_client` returns an instance of the MinioClient class initialized with a
    provided configuration.
    :return: An instance of the MinioClient class initialized with the minio_config parameter.
    """
    return MinioClient(minio_config)
