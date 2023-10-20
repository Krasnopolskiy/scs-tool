from http import HTTPStatus

from aiohttp import ClientSession
from loguru import logger

from etherscan.urls import Endpoint, reverse


async def fetch_contract_html(transaction_id: str) -> str:
    """
    The function retrieves the HTML content of a contract using a transaction ID.

    :param transaction_id: The `transaction_id` parameter is a string that represents the unique
    identifier of a transaction. It is used to construct the URL for retrieving the contract HTML
    :type transaction_id: str
    :return: The function `retrieve_contract_html` returns a string, which is the HTML content of the
    contract retrieved from the specified transaction ID.
    """
    async with ClientSession() as session:
        logger.info("Fetching transaction {}", transaction_id)
        url = reverse(Endpoint.TRANSACTION, transaction_id=transaction_id)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("Error during transaction {} fetching: {}: {}", transaction_id, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("Transaction {} fetched successfully", transaction_id)
            return text
