import asyncio
from asyncio import Task

from analyzers.semgrep.semgrep import analyze
from analyzers.semgrep.writers import write_report_files
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions
async def analyze_address(address: Address):
    """
    The `analyze_addresses` function asynchronously analyzes a list of addresses and writes report files
    for each address.

    :param address: The `address` parameter in the `analyze_address` function is of type `Address`,
    which represents a single address that needs to be analyzed
    :type address: Address
    """
    output = await analyze(address)
    write_report_files(address, output)


async def analyze_addresses(addresses: list[Address]):
    """
    The `analyze_addresses` function asynchronously analyzes a list of addresses using the
    `analyze_address` function.

    :param addresses: A list of Address objects
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
    for address in addresses:
        task = asyncio.ensure_future(analyze_address(address))
        tasks.append(task)
    await asyncio.gather(*tasks)
