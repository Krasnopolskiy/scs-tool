import asyncio
from asyncio import Task

from analyzers.slither.slither import analyze
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions()
async def analyze_address(address: Address):
    """
    This Python function `analyze_address` asynchronously analyzes an address and writes a report based
    on the analysis.

    :param address: The `analyze_address` function is an asynchronous function that takes an `Address`
    object as a parameter. The function awaits the result of the `analyze` function with the given
    address and then writes a report based on the analysis
    :type address: Address
    """
    report = await analyze(address)
    report.write(address)


async def analyze_addresses(addresses: list[Address]):
    """
    The function `analyze_addresses` asynchronously analyzes a list of addresses using `analyze_address`
    function.

    :param addresses: It looks like the `analyze_addresses` function is designed to take a list of
    `Address` objects as input. The function then creates a list of tasks using asyncio to analyze each
    address concurrently. The `analyze_address` function is likely an asynchronous function that
    performs some analysis on a single address
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
    for address in addresses:
        task = asyncio.ensure_future(analyze_address(address))
        tasks.append(task)
    await asyncio.gather(*tasks)
