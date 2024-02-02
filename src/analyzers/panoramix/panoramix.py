import sys

from loguru import logger
from panoramix.decompiler import Decompilation, decompile_bytecode

from common.config.constants import BYTECODE_FILE, SOURCE_PATH
from common.schemas import Address

sys.set_int_max_str_digits(2**20)


async def decompile(address: Address) -> Decompilation:
    """
    The `decompile` function takes an address, reads the bytecode from a file, and returns the
    decompiled code.

    :param address: The `address` parameter is the address of the smart contract that you want to
    decompile
    :type address: Address
    :return: The function `decompile` is returning a `Decompilation` object.
    """
    target = SOURCE_PATH / address / BYTECODE_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Running panoramix decompilation on {}", address)
    with target.open("rb") as contract:
        code = contract.read().hex()
        return decompile_bytecode(code)
