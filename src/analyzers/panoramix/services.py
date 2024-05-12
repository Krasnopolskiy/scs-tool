import asyncio
from asyncio import Task

from analyzers.panoramix.panoramix import decompile
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions()
async def decompile_address(address: Address):
    """
    This Python function asynchronously decompiles an address and writes the decompiled files.

    :param address: It looks like you have a function `decompile_address` that takes an `Address` object
    as a parameter. The function is asynchronous and it calls a `decompile` function to decompile the
    address. After decompiling, it iterates over the decompiled files and writes the address to
    :type address: Address
    """
    decompiled = await decompile(address)
    for file in decompiled:
        file.write(address)


async def decompile_addresses(addresses: list[Address]):
    """
    The function `decompile_addresses` takes a list of `Address` objects, creates a list of tasks to
    decompile each address asynchronously, and then waits for all tasks to complete.

    :param addresses: A list of Address objects
    :type addresses: list[Address]
    """
    tasks: list[Task] = []
    for address in addresses:
        task = asyncio.ensure_future(decompile_address(address))
        tasks.append(task)
    await asyncio.gather(*tasks)
