from loguru import logger

from common.constants import SOURCE_PATH
from common.schemas import Address, ContractFile


def write_contract_files(address: Address, files: list[ContractFile]):
    """
    The function `write_contract_files` writes a list of contract files to a specified address.

    :param address: The `address` parameter is of type `Address` and represents the address of a
    contract
    :type address: Address
    :param files: The `files` parameter is a list of `ContractFile` objects. Each `ContractFile` object
    represents a file that needs to be written. It has two attributes:
    :type files: list[ContractFile]
    :return: If the `files` list is empty, the function will return without performing any further
    actions.
    """
    logger.info("Writing {} files from contract {}", len(files), address)
    if not files:
        return
    path = SOURCE_PATH / address
    path.mkdir(parents=True, exist_ok=True)
    for file in files:
        with open(f"{path}/{file.name}", "w", encoding="utf-8") as out:
            out.write(file.content)
    logger.info("Contract {} files saved to the {}", address, path)
