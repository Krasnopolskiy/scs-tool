import re
from dataclasses import dataclass
from pathlib import Path

from panoramix.decompiler import Decompilation

from analyzers.panoramix.constants import PSEUDOCODE_FILE, ASSEMBLER_FILE
from common.config.constants import SOURCE_PATH, BYTECODE_PATH
from common.schemas import BaseFile, Address

color_regex = re.compile(r"\x1b\[[\d;]+m")


@dataclass
class ContractPseudocodeFile(BaseFile[Decompilation]):
    name: str = PSEUDOCODE_FILE

    def get_path(self, address: Address) -> Path:
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        return re.sub(color_regex, "", self.content.text)


@dataclass
class ContractAssemblerFile(BaseFile[Decompilation]):
    name: str = ASSEMBLER_FILE

    def get_path(self, address: Address) -> Path:
        return SOURCE_PATH / address / BYTECODE_PATH / self.name

    def get_content(self) -> str:
        return "\n".join(self.content.asm)
