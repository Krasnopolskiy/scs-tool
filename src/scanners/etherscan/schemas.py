from dataclasses import dataclass, field
from pathlib import Path

from common.constants import BYTECODE_FILE, BYTECODE_PATH, SOURCE_PATH
from common.schemas import Address, BaseFile


@dataclass
class ContractSourceFile(BaseFile[str]):
    pass


@dataclass
class ContractByteFile(BaseFile[bytes]):
    name: str = BYTECODE_FILE
    write_params: dict = field(default_factory=lambda: {"mode": "wb"})

    def get_path(self, address: Address) -> Path:
        """
        The function `get_path` returns a path based on the given address, bytecode path, and name.

        :param address: The `address` parameter in the `get_path` method is an instance of the `Address`
        class. It is used to construct a file path by appending it to other path components like
        `SOURCE_PATH`, `BYTECODE_PATH`, and the name of the object (`self.name`)
        :type address: Address
        :return: A Path object representing the path to the bytecode file associated with the given
        address and the name of the object.
        """
        return SOURCE_PATH / address / BYTECODE_PATH / self.name
