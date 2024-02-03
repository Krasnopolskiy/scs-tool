import sys

from loguru import logger
from panoramix.decompiler import decompile_bytecode

from analyzers.panoramix.schemas import ContractPseudocodeFile, ContractAssemblerFile
from common.config.constants import BYTECODE_FILE, SOURCE_PATH
from common.schemas import Address

sys.set_int_max_str_digits(2**20)


async def decompile(address: Address) -> tuple[ContractPseudocodeFile, ContractAssemblerFile]:
    target = SOURCE_PATH / address / BYTECODE_FILE
    if not target.exists():
        logger.info("[{}] Nothing to decompile", address)
        return tuple()
    logger.info("[{}] Running panoramix decompilation", address)
    with target.open("rb") as contract:
        code = contract.read().hex()
        decompilation = decompile_bytecode(code)
    return ContractPseudocodeFile(content=decompilation), ContractAssemblerFile(content=decompilation)
