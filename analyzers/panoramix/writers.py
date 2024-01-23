import re

from loguru import logger
from panoramix.decompiler import Decompilation

from common.constants import BYTECODE_PATH, SOURCE_PATH
from common.schemas import Address

color_regex = re.compile(r"\x1b\[[\d;]+m")


def write_decompiled_files(address: Address, decompilation: Decompilation):
    """
    The function `write_decompiled_files` writes decompiled Solidity code and assembly code to text and
    ASM files respectively.

    :param address: The `address` parameter is the address of the contract for which the decompiled
    files are being written
    :type address: Address
    :param decompilation: The `decompilation` parameter is an object of type `Decompilation`. It
    contains the decompiled text and assembly code of a contract
    :type decompilation: Decompilation
    """
    text_file = SOURCE_PATH / address / BYTECODE_PATH / "decompiled.sol"
    asm_file = SOURCE_PATH / address / BYTECODE_PATH / "decompiled.asm"
    with text_file.open("w", encoding="utf-8") as out:
        text = re.sub(color_regex, "", decompilation.text)
        out.write(text)
    with asm_file.open("w", encoding="utf-8") as out:
        asm = "\n".join(decompilation.asm)
        out.write(asm)
    logger.info("Contract {} files {}, {} saved", address, text_file.name, asm_file.name)
