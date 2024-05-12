import re
from dataclasses import dataclass
from pathlib import Path

from panoramix.decompiler import Decompilation

from analyzers.panoramix.constants import ASSEMBLER_FILE, PSEUDOCODE_FILE
from common.constants import BYTECODE_PATH, SOURCE_PATH
from common.schemas import Address, BaseFile

COLOR = re.compile(r"\x1b\[[\d;]+m")


@dataclass
class ContractPseudocodeFile(BaseFile[Decompilation]):
    name: str = PSEUDOCODE_FILE

    def get_path(self, address: Address) -> Path:
        """
        The function `get_path` returns a path based on the given address, bytecode path, and name.

        :param address: The `address` parameter in the `get_path` method is of type `Address`. It is
        used to specify the address for which the path is being generated
        :type address: Address
        :return: a Path object that represents the path to a specific file. The path is constructed
        using the SOURCE_PATH, address, BYTECODE_PATH, and the name attribute of the object.
        """
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        """
        The function `get_content` removes color codes from the text content.
        :return: The `get_content` method is returning the content text with any color codes removed.
        """
        return re.sub(COLOR, "", self.content.text)


@dataclass
class ContractAssemblerFile(BaseFile[Decompilation]):
    name: str = ASSEMBLER_FILE

    def get_path(self, address: Address) -> Path:
        """
        This function returns a path based on the given address and the name of the object.

        :param address: The `address` parameter in the `get_path` method is an instance of the `Address`
        class. It is used to construct a file path by appending it to other path components like
        `SOURCE_PATH`, `BYTECODE_PATH`, and the name of the object (`self.name`)
        :type address: Address
        :return: A Path object representing the path to the bytecode file associated with the given
        address and the name of the object.
        """
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        """
        The function `get_content` returns the content of the `asm` attribute of the object, joined by
        newline characters.
        :return: The `get_content` method is returning a string that is created by joining the elements
        of the `asm` attribute of the `content` object with newline characters in between each element.
        """
        return "\n".join(self.content.asm)
