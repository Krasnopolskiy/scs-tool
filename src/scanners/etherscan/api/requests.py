import json
from http import HTTPStatus

from loguru import logger

from common.schemas import Address, Transaction
from scanners.etherscan.api.schemas import ContractSourceResponse
from scanners.etherscan.api.urls import Endpoint, reverse
from scanners.etherscan.config.client import session_builder


async def fetch_contract_page(address: Address) -> str:
    """
    This Python async function fetches a contract page using an address and returns the text content of
    the page.

    :param address: The `address` parameter in the `fetch_contract_page` function is expected to be of
    type `Address`. It is used to specify the address of the contract for which the page needs to be
    fetched
    :type address: Address
    :return: The function `fetch_contract_page` is returning a string, which is the text content of the
    contract page fetched from the specified address.
    """
    async with session_builder.session() as session:
        logger.info("[{}] Fetching contract", address)
        url = reverse(Endpoint.ADDRESS, address=address)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("[{}] Error during fetching contract {}: {}", address, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("[{}] Contract fetched successfully", address)
            return text


async def fetch_transaction_page(transaction: Transaction) -> str:
    """
    This async function fetches a transaction page using a session and returns the text content if the
    response status is OK.

    :param transaction: The `transaction` parameter in the `fetch_transaction_page` function is an
    instance of the `Transaction` class. It is used to identify the specific transaction that needs to
    be fetched from a remote server
    :type transaction: Transaction
    :return: The function `fetch_transaction_page` returns the text content of the response from the
    HTTP GET request made to the specified URL for the given transaction.
    """
    async with session_builder.session() as session:
        logger.info("[{}] Fetching transaction", transaction)
        url = reverse(Endpoint.TRANSACTION, transaction=transaction)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("[{}] Error during fetching transaction {}: {}", transaction, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("[{}] Transaction fetched successfully", transaction)
            return text


async def fetch_contract_source_code(address: Address) -> ContractSourceResponse:
    """
    This Python async function fetches contract source code from a specified address using an API
    endpoint and returns a ContractSourceResponse object.

    :param address: The `address` parameter in the `fetch_contract_source_code` function is expected to
    be of type `Address`. This parameter likely represents the address of a smart contract on the
    blockchain from which you want to fetch the corresponding source code
    :type address: Address
    :return: The function `fetch_contract_source_code` is returning a `ContractSourceResponse` object.
    """
    async with session_builder.session() as session:
        logger.info("[{}] Fetching source code", address)
        url = reverse(Endpoint.SOURCE_CODE, address=address, key=session_builder.apikey)
        async with session.get(url) as response:
            text = await response.text()
            if response.status != HTTPStatus.OK:
                logger.error("[{}] Error during fetching source code {}: {}", address, response.status, text)
                raise IOError(f"Server returned {response.status}: {text}")
            logger.info("[{}] Source code fetched successfully", address)
            data = json.loads(text)
            return ContractSourceResponse(**data)
