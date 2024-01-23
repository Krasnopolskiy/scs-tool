from abc import ABC
from dataclasses import dataclass, field
from typing import Annotated

from pydantic import Field

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
