import re

from loguru import logger
from panoramix.decompiler import Decompilation

from common.constants import SOURCE_PATH
from common.schemas import Address

color_regex = re.compile(r"\x1b\[[\d;]+m")


def write_decompiled_files(address: Address, decompilation: Decompilation):
    """
    The function `write_decompiled_files` writes the decompiled text and assembly code to separate
    files.

    :param address: The `address` parameter is the address of the file or directory where the decompiled
    files will be written to
    :type address: Address
    :param decompilation: The `decompilation` parameter is an object of type `Decompilation`. It
    contains the decompiled text and assembly code
    :type decompilation: Decompilation
    """
    text_file = SOURCE_PATH / address / "decompiled.txt"
    asm_file = SOURCE_PATH / address / "decompiled.asm"
    with text_file.open("w", encoding="utf-8") as out:
        text = re.sub(color_regex, "", decompilation.text)
        out.write(text)
    with asm_file.open("w", encoding="utf-8") as out:
        asm = "\n".join(decompilation.asm)
        out.write(asm)
    logger.info("Writing {}, {}", text_file, asm_file)
