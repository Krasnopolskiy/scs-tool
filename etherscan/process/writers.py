from pathlib import Path

from loguru import logger

from common.schemas import Address, ContractFile
from etherscan.config.constants import SOURCE_PATH


def write_contract_files(address: Address, files: list[ContractFile]):
    """
    The function `write_contract_files` writes a list of contract files to a specified directory,
    creating the directory if it doesn't exist.

    :param address: The `address` parameter is of type `Address`, which is likely a custom data type
    representing a contract address
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
    directory = SOURCE_PATH + address
    Path(directory).mkdir(parents=True, exist_ok=True)
    for file in files:
        with open(f"{directory}/{file.name}", "w", encoding="utf-8") as out:
            out.write(file.content)
    logger.info("Contract {} files saved to the {}", address, directory)
