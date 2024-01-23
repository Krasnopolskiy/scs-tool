from loguru import logger

from common.constants import SOURCE_PATH
from common.schemas import Address, ContractBaseFile


def write_contract_files(address: Address, files: list[ContractBaseFile]):
    """
    The function `write_contract_files` writes a list of contract files to a specified address.

    :param address: The `address` parameter is the address of the contract. It is of type `Address`
    :type address: Address
    :param files: A list of ContractBaseFile objects, which represent the files to be written. Each
    ContractBaseFile object has the following attributes:
    :type files: list[ContractBaseFile]
    :return: If the `files` list is empty, the function will return without performing any further
    actions.
    """
    logger.info("Writing {} files from contract {}", len(files), address)
    if not files:
        return
    path = SOURCE_PATH / address
    for file in files:
        target = path / file.name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open(**file.write_params) as out:
            out.write(file.content)
    logger.info("Contract {} files saved", address)
