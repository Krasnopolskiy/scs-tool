import asyncio
from asyncio import Task

from common.schemas import Address, Transaction
from common.utils import handle_exceptions
from scanners.etherscan.api.requests import fetch_contract_page, fetch_contract_source_code, fetch_transaction_page
from scanners.etherscan.parsers import (
    parse_contract_bytecode,
    parse_contract_files,
    parse_contract_source_response,
    parse_transaction,
)


async def scan_addresses(addresses: list[Address]):
    """
    The function `scan_addresses` asynchronously processes a list of addresses.

    :param addresses: A list of Address objects
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
    for address in addresses:
        task = asyncio.ensure_future(process_address_source(address))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def load_transactions_addresses(transactions: list[Transaction]) -> list[Address]:
    """
    The function `load_transactions_addresses` asynchronously loads the addresses associated with a list
    of transactions.

    :param transactions: A list of Transaction objects
    :type transactions: list[Transaction]
    :return: The function `load_transactions_addresses` returns a list of `Address` objects.
    """
    tasks: list[Task] = []
    for transaction in transactions:
        task = asyncio.ensure_future(load_transaction_addresses(transaction))
        tasks.append(task)
    addresses: list[Address] = []
    for result in await asyncio.gather(*tasks):
        addresses.extend(result)
    return addresses


@handle_exceptions()
async def process_address(address: Address):
    """
    This Python function processes an address by fetching a contract page, parsing contract files and
    bytecode, and writing the files with the address.

    :param address: Address is a data structure that represents a physical or network address. It
    typically includes fields such as street address, city, state, postal code, and country for physical
    addresses, or IP address and port number for network addresses. In the context of the provided code
    snippet, the `process_address` function
    :type address: Address
    """
    page = await fetch_contract_page(address)
    sources = parse_contract_files(page)
    bytecode = parse_contract_bytecode(page, address)
    for file in sources + bytecode:
        file.write(address)


@handle_exceptions()
async def process_address_source(address: Address):
    """
    This Python function processes the source code of a contract associated with a given address.

    :param address: Address is an object representing the address of a smart contract on the blockchain
    :type address: Address
    """
    response = await fetch_contract_source_code(address)
    sources = parse_contract_source_response(response)
    for file in sources:
        file.write(address)


@handle_exceptions(default=[])
async def load_transaction_addresses(transaction: Transaction) -> list[Address]:
    """
    The function `load_transaction_addresses` loads a transaction page and parses it to extract a list
    of addresses.

    :param transaction: The `transaction` parameter is an instance of the `Transaction` class
    :type transaction: Transaction
    :return: The function `load_transaction_addresses` returns a list of `Address` objects.
    """
    page = await fetch_transaction_page(transaction)
    return parse_transaction(page)
