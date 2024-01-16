import asyncio
from asyncio import Task

from analyzers.panoramix.panoramix import decompile
from analyzers.panoramix.writers import write_decompiled_files
from common.schemas import Address
from common.utils import handle_exceptions


@handle_exceptions
async def decompile_address(address: Address):
    """
    The `decompile_addresses` function asynchronously decompiles a list of addresses and writes the
    decompiled files.

    :param address: The `address` parameter in the `decompile_address` function is of type `Address`. It
    represents a single address that needs to be decompiled
    :type address: Address
    """
    decompilation = await decompile(address)
    write_decompiled_files(address, decompilation)


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
