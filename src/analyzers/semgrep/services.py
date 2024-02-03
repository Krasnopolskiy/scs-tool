import asyncio
from asyncio import Task

from analyzers.semgrep.semgrep import analyze
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions
async def analyze_address(address: Address):
    report = await analyze(address)
    report.write(address)


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
