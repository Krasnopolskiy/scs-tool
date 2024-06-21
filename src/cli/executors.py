import asyncio
from argparse import Namespace
from asyncio import Task

import nest_asyncio

from analyzers.mythril.services import analyze_addresses as mythril_analyzes
from analyzers.panoramix.services import decompile_addresses
from analyzers.semgrep.services import analyze_addresses as semgrep_analyzes
from analyzers.slither.services import analyze_addresses as slither_analyzes
from cli.parsers import parser
from common.schemas import Address
from scanners.etherscan.services import load_transactions_addresses, scan_addresses
from scanners.local.services import load_local_addresses


async def get_addresses(args: Namespace) -> list[Address]:
    """
    The function `get_addresses` asynchronously retrieves addresses based on the provided arguments.

    :param args: Namespace object containing arguments passed to the function. It may include
    'addresses' and 'transactions' attributes
    :type args: Namespace
    :return: The function `get_addresses` returns a list of `Address` objects.
    """
    tasks: list[Task] = []

    if args.addresses:

        async def get_args_addresses():
            return args.addresses

        tasks.append(asyncio.ensure_future(get_args_addresses()))

    if args.transactions:
        tasks.append(asyncio.ensure_future(load_transactions_addresses(args.transactions)))

    if args.local:
        tasks.append(asyncio.ensure_future(load_local_addresses()))

    addresses: list[Address] = []
    for result in await asyncio.gather(*tasks):
        addresses.extend(result)
    return addresses


async def scan(args: Namespace, addresses: list[Address]):
    """
    The `scan` function is an asynchronous function that scans a list of addresses using the
    `scan_addresses` function if the `etherscan` argument is provided.

    :param args: Namespace object containing command-line arguments passed to the script
    :type args: Namespace
    :param addresses: A list of addresses to be scanned
    :type addresses: list[Address]
    """
    if args.etherscan:
        await scan_addresses(addresses)


async def analyze(args: Namespace, addresses: list[Address]):
    """
    The `analyze` function asynchronously performs various analyses on a list of addresses based on the
    provided arguments.

    :param args: Namespace object containing command-line arguments parsed by argparse
    :type args: Namespace
    :param addresses: The `addresses` parameter in the `analyze` function is a list of `Address`
    objects. These objects likely represent addresses that need to be analyzed in some way, such as in
    the context of security analysis tools like Semgrep, Mythril, and Slither. The function processes
    these addresses based
    :type addresses: list[Address]
    """
    nest_asyncio.apply()
    if args.decompile:
        await decompile_addresses(addresses)

    tasks = []
    if args.semgrep:
        tasks.append(semgrep_analyzes(addresses))
    if args.mythril:
        tasks.append(mythril_analyzes(addresses))
    if args.slither:
        tasks.append(slither_analyzes(addresses))

    await asyncio.gather(*tasks)


async def execute():
    """
    The `execute` function parses arguments, gets addresses, scans them, and analyzes them.
    """
    args = parser.parse_args()
    addresses = await get_addresses(args)
    await scan(args, addresses)
    await analyze(args, addresses)
