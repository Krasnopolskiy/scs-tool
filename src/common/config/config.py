from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class PathConfig(BaseSettings):
    """
    The `PathConfig` class is a subclass of `BaseSettings` that defines a configuration setting
    `base_path` of type `Path` with a default value of `"."`.
    """

    base_path: Path = Path(".")


class MinioConfig(BaseSettings):
    """
    The `MinioConfig` class is a configuration class that represents the settings for connecting to a
    MinIO server.
    """

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
