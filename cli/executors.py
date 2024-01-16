import asyncio
from argparse import Namespace
from asyncio import Task

import nest_asyncio

from analyzers.panoramix.services import decompile_addresses
from analyzers.semgrep.services import analyze_addresses
from cli.parsers import parser
from common.schemas import Address
from scanners.etherscan.services import load_addresses, load_transactions_addresses, scan_addresses


async def get_addresses(args: Namespace) -> list[Address]:
    """
    The function `get_addresses` retrieves a list of addresses based on the provided arguments.

    :param args: The `args` parameter is of type `Namespace`, which is typically an object that holds
    command-line arguments parsed by an argument parser. It contains the values of the command-line
    arguments passed to the program
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
    if args.last:
        tasks.append(asyncio.ensure_future(load_addresses(args.last)))
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
    The `analyze` function analyzes a list of addresses using semgrep.

    :param args: Namespace object that contains the command-line arguments passed to the program
    :type args: Namespace
    :param addresses: A list of Address objects
    :type addresses: list[Address]
    """
    nest_asyncio.apply()
    if args.analyze:
        await analyze_addresses(addresses)
    if args.decompile:
        await decompile_addresses(addresses)


async def execute():
    """
    The `execute` function parses arguments, gets addresses, scans them, and analyzes them.
    """
    args = parser.parse_args()
    addresses = await get_addresses(args)
    await scan(args, addresses)
    await analyze(args, addresses)
