import asyncio
from asyncio import Task

from analyzers.semgrep.process.loggers import log_report
from analyzers.semgrep.process.writers import write_report_files
from analyzers.semgrep.semgrep import analyze
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions
async def analyze_address(address: Address):
    """
    The `analyze_address` function takes an address, analyzes it, writes report files, and logs the
    report.

    :param address: The `address` parameter is an instance of the `Address` class. It represents a
    physical address and contains properties such as street, city, state, and zip code
    :type address: Address
    """
    output = await analyze(address)
    write_report_files(address, output)
    log_report(output)


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
