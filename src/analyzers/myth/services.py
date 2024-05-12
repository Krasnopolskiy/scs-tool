import asyncio
from asyncio import Task

from analyzers.myth.myth import analyze
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions()
async def analyze_address(address: Address):
    """
    This Python function `analyze_address` asynchronously analyzes an address and writes a report based
    on the analysis.

    :param address: The `analyze_address` function is an asynchronous function that takes an `Address`
    object as a parameter. The function calls the `analyze` function asynchronously to generate a report
    based on the provided address. Finally, the report is written using the `write` method of the report
    object
    :type address: Address
    """
    report = await analyze(address)
    report.write(address)


async def analyze_addresses(addresses: list[Address]):
    """
    The function `analyze_addresses` asynchronously analyzes a list of addresses using `analyze_address`
    function.

    :param addresses: The `addresses` parameter is a list of `Address` objects. Each `Address` object
    likely contains information about a specific address, such as street name, city, state, and postal
    code. The `analyze_addresses` function takes a list of these `Address` objects and asynchronously
    analyzes each address
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
    for address in addresses:
        task = asyncio.ensure_future(analyze_address(address))
        tasks.append(task)
    await asyncio.gather(*tasks)
