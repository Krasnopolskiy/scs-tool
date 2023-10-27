from argparse import ArgumentParser

from cli.types import address_type, transactions_number_type

parser = ArgumentParser(
    description="Blockchain Contract Parser",
)
parser.add_argument(
    "-a",
    "--addresses",
    nargs="+",
    type=address_type,
    help="List of address IDs containing the contracts to be parsed",
)
parser.add_argument(
    "-l",
    "--last",
    type=transactions_number_type,
    help="The number of last transactions containing contracts to be parsed <= 100_000",
)
