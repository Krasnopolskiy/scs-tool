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
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        return re.sub(COLOR, "", self.content.text)


@dataclass
class ContractAssemblerFile(BaseFile[Decompilation]):
    name: str = ASSEMBLER_FILE

    def get_path(self, address: Address) -> Path:
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        return "\n".join(self.content.asm)
