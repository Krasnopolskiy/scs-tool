import asyncio

from cli.parsers import parser
from etherscan.service import process_addresses, process_last_addresses, process_transactions


async def etherscan():
    """
    The function takes command line arguments, processes addresses and last addresses
    asynchronously, and waits for all tasks to complete.
    """
    tasks = []
    args = parser.parse_args()
    if args.addresses:
        tasks.append(asyncio.ensure_future(process_addresses(args.addresses)))
    if args.transactions:
        tasks.append(asyncio.ensure_future(process_transactions(args.transactions)))
    if args.last:
        tasks.append(asyncio.ensure_future(process_last_addresses(args.last)))
    await asyncio.gather(*tasks)
