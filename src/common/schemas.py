from abc import ABC
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated

from pydantic import Field

from common.config.constants import BYTECODE_PATH

Address = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{40}$")]
Transaction = Annotated[str, Field(pattern=r"^0x[a-fA-F0-9]{64}$")]


@dataclass
class ContractBaseFile(ABC):
    """
    The `ContractBaseFile` class represents a contract file with a name, content, and write parameters.
    """

    name: str
    content: str | bytes
    write_params: dict

    def get_path(self, path: Path) -> Path:
        """
        The function takes a path and returns a new path by appending the name of the object.
        
        :param path: The `path` parameter is of type `Path`. It represents a file or directory path
        :type path: Path
        :return: the concatenation of the input `path` and the `name` attribute of the object.
        """
        return path / self.name


@dataclass
class ContractSourceFile(ContractBaseFile):
    """
    The `ContractSourceFile` class is a subclass of `ContractBaseFile` that represents a source file and contains a
    content string and write parameters.
    """

    content: str
    write_params: dict = field(default_factory=lambda: {"mode": "w", "encoding": "utf-8"})


@dataclass
class ContractByteFile(ContractBaseFile):
    """
    The `ContractByteFile` class is a subclass of `ContractBaseFile` that represents a contract file with content stored
    as bytes and includes write parameters.
    """

    content: bytes
    write_params: dict = field(default_factory=lambda: {"mode": "wb"})

    def get_path(self, path: Path) -> Path:
        """
        The function returns the path to a bytecode file by appending the bytecode path and the name of
        the object.
        
        :param path: The `path` parameter is of type `Path`. It represents the base directory path where
        the file will be located
        :type path: Path
        :return: the concatenation of the `path`, `BYTECODE_PATH`, and `self.name` as a `Path` object.
        """
        return path / BYTECODE_PATH / self.name
