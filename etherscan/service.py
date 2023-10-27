import asyncio

from common.schemas import Address
from etherscan.client.requests import fetch_contract_page, fetch_transaction_list_page
from etherscan.config import constants
from etherscan.process.parsers import parse_contract_files, parse_transaction_list
from etherscan.process.writers import write_contract_files


async def process_last_addresses(size: int):
    """
    The function `process_last_addresses` loads a specified number of addresses and then processes them.
    
    :param size: The size parameter represents the number of addresses to load and request
    :type size: int
    """
    addresses = await load_addresses(size)
    await process_addresses(addresses)


async def process_addresses(addresses: list[Address]):
    """
    The function `process_addresses` takes a list of addresses and processes each address concurrently
    using asyncio.
    
    :param addresses: The `addresses` parameter is a list of `Address` objects
    :type addresses: list[Address]
    """
    tasks = []
    for address in addresses:
        task = asyncio.ensure_future(process_address(address))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def process_address(address: Address):
    """
    The function `process_address` fetches a contract page using an address, parses the contract files
    from the page, and writes the contract files to a location.
    
    :param address: The `address` parameter is an instance of the `Address` class. It represents the
    address of a contract
    :type address: Address
    """
    page = await fetch_contract_page(address)
    files = parse_contract_files(page)
    write_contract_files(address, files)


async def load_addresses(size: int) -> list[Address]:
    """
    The function `load_addresses` asynchronously loads a list of addresses by making multiple requests
    with a specified size and returns the combined result.
    
    :param size: The `size` parameter represents the total number of addresses to load
    :type size: int
    :return: The function `load_addresses` returns a list of `Address` objects.
    """
    tasks = []
    for offset in range(0, size, constants.PAGE_SIZE):
        tasks.append(asyncio.ensure_future(list_transactions(offset)))
    await asyncio.gather(*tasks)
    return [address for task in tasks for address in task.result()]


async def list_transactions(offset: int) -> list[Address]:
    """
    The function `list_transactions` retrieves a list of transactions from a remote source and returns a
    parsed list of addresses.
    
    :param offset: The offset parameter is an integer that represents the starting index of the
    transactions to retrieve. It is used to paginate through the list of transactions
    :type offset: int
    :return: a list of Address objects.
    """
    page = await fetch_transaction_list_page(constants.PAGE_SIZE, offset)
    return parse_transaction_list(page)
