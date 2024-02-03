from dataclasses import dataclass, field
from pathlib import Path

from common.config.constants import BYTECODE_PATH, BYTECODE_FILE, SOURCE_PATH
from common.schemas import BaseFile, Address


@dataclass
class ContractSourceFile(BaseFile[str]):
    pass


@dataclass
class ContractByteFile(BaseFile[bytes]):
    name: str = BYTECODE_FILE
    write_params: dict = field(default_factory=lambda: {"mode": "wb"})

    def get_path(self, address: Address) -> Path:
        return SOURCE_PATH / address / BYTECODE_PATH / self.name
