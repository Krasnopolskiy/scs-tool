from loguru import logger

from common.config.constants import SOURCE_PATH
from common.minio import MinioClient
from common.schemas import Address, ContractBaseFile

minio = MinioClient()


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
    if not files:
        logger.warning("No files for {} saved", address)
        return
    logger.info("Writing {} files from contract {}", len(files), address)
    path = SOURCE_PATH / address
    for file in files:
        target = file.get_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open(**file.write_params) as out:
            out.write(file.content)
        minio.write(target, file.content)
    logger.info("Contract {} files saved", address)
