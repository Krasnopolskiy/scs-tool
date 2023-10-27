from http import HTTPStatus

from loguru import logger

from common.schemas import Address
from etherscan.client.urls import Endpoint, reverse
from etherscan.config.client import ClientSessionBuilder


async def fetch_contract_page(address: Address) -> str:
    """
    The function fetches a contract page from a given address using an asynchronous HTTP client session.

    :param address: The `address` parameter is of type `Address`. It represents the address of a
    contract
    :type address: Address
    :return: The function `fetch_contract_page` returns a string.
    """
    async with ClientSessionBuilder().session() as session:
        logger.info("Fetching contract {}", address)
        url = reverse(Endpoint.ADDRESS, address=address)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("Error during fetching contract {}: {}: {}", address, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("Contract {} fetched successfully", address)
            return text


async def fetch_transaction_list_page(size: int, offset: int) -> str:
    """
    The function fetches a list of transactions from a specified offset with a specified size using an
    HTTP GET request.

    :param size: The `size` parameter represents the number of transactions to fetch in a single page.
    It determines the number of transactions that will be returned in the response
    :type size: int
    :param offset: The `offset` parameter is used to specify the starting index of the transactions to
    fetch. It determines the position in the list of transactions from where the fetching should begin
    :type offset: int
    :return: The function `fetch_transaction_list_page` returns a string.
    """
    async with ClientSessionBuilder().session() as session:
        logger.info("Fetching list addresses from {} to {}", offset, offset + size)
        url = reverse(Endpoint.TRANSACTION_LIST, size=size, offset=offset)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("Error during fetching list transactions {}: {}", offset, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("Transactions list from {} to {} fetched successfully", offset, offset + size)
            return text
