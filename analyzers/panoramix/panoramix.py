import sys

from loguru import logger
from panoramix.decompiler import Decompilation, decompile_bytecode

from common.constants import BYTECODE_FILE, SOURCE_PATH
from common.schemas import Address

sys.set_int_max_str_digits(430000)


async def decompile(address: Address) -> Decompilation:
    """
    The `decompile` function takes an address as input, reads the bytecode from a file, and returns the
    decompiled code.

    :param address: The `address` parameter is of type `Address`. It represents the address of a
    contract in the blockchain
    :type address: Address
    :return: a `Decompilation` object.
    """
    target = SOURCE_PATH / address / BYTECODE_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Running panoramix decompilation on {}", address)
    with target.open("r", encoding="utf-8") as contract:
        code = contract.read()
        return decompile_bytecode(code)
