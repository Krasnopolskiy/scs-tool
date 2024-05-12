import sys

from loguru import logger
from panoramix.decompiler import decompile_bytecode

from analyzers.panoramix.schemas import ContractAssemblerFile, ContractPseudocodeFile
from common.constants import BYTECODE_FILE, SOURCE_PATH
from common.schemas import Address

sys.set_int_max_str_digits(2**20)


async def decompile(address: Address) -> tuple[ContractPseudocodeFile, ContractAssemblerFile]:
    """
    This Python async function decompiles bytecode from a specified address and returns the decompiled
    content as both pseudocode and assembler files.

    :param address: Address of the smart contract bytecode that needs to be decompiled
    :type address: Address
    :return: The function `decompile` returns a tuple containing a `ContractPseudocodeFile` object with
    the decompiled content and a `ContractAssemblerFile` object with the same decompiled content.
    """
    target = SOURCE_PATH / address / BYTECODE_FILE
    if not target.exists():
        logger.info("[{}] Nothing to decompile", address)
        return tuple()
    logger.info("[{}] Running panoramix decompilation", address)
    with target.open("rb") as contract:
        code = contract.read().hex()
        decompiled = decompile_bytecode(code)
    return ContractPseudocodeFile(content=decompiled), ContractAssemblerFile(content=decompiled)
