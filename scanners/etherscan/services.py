import asyncio
from asyncio import Task

from common.schemas import Address, Transaction
from scanners.etherscan.client.requests import fetch_contract_page, fetch_transaction_list_page, fetch_transaction_page
from scanners.etherscan.config import constants
from scanners.etherscan.process.parsers import parse_contract_files, parse_transaction_list, parse_transaction
from scanners.etherscan.process.writers import write_contract_files


async def scan_addresses(addresses: list[Address]):
    """
    The function `scan_addresses` asynchronously processes a list of addresses.
    
    :param addresses: A list of Address objects
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
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


async def load_addresses(size: int) -> list[Address]:
    """
    The function `load_addresses` asynchronously loads a list of addresses by dividing the task into
    multiple pages and using `list_transactions` to retrieve the addresses for each page.
    
    :param size: The `size` parameter represents the total number of addresses to load
    :type size: int
    :return: The function `load_addresses` returns a list of `Address` objects.
    """
    tasks: list[Task] = []
    page = min(size, constants.PAGE_SIZE)
    for offset in range(0, size, constants.PAGE_SIZE):
        tasks.append(asyncio.ensure_future(list_transactions(page, offset)))
    await asyncio.gather(*tasks)
    return [address for task in tasks for address in task.result()]


async def list_transactions(size: int, offset: int) -> list[Address]:
    """
    The function `list_transactions` retrieves a specified number of transactions from a transaction
    list, starting from a given offset.
    
    :param size: The `size` parameter represents the number of transactions to retrieve in each page of
    the transaction list
    :type size: int
    :param offset: The offset parameter is used to specify the starting index of the transactions to be
    retrieved. It determines the position from which the transactions will be fetched in the list
    :type offset: int
    :return: a list of Address objects.
    """
    page = await fetch_transaction_list_page(size, offset)
    return parse_transaction_list(page)[:size]