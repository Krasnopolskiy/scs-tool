from argparse import ArgumentParser

from cli.types import address_type, transactions_number_type, transaction_type

parser = ArgumentParser(
    description="Blockchain Contract Parser",
)

scanner = parser.add_argument_group(title="Address loader options")
scanner.add_argument(
    "-a",
    "--addresses",
    nargs="+",
    type=address_type,
    help="List of address IDs containing the contracts to be parsed",
)
scanner.add_argument(
    "-t",
    "--transactions",
    nargs="+",
    type=transaction_type,
    help="List of transactions IDs containing the contracts to be parsed",
)
scanner.add_argument(
    "-l",
    "--last",
    type=transactions_number_type,
    help="The number of last transactions containing contracts to be parsed <= 100_000",
)

analyzer = parser.add_argument_group(title="Scanner options")
analyzer.add_argument(
    "--etherscan",
    help="Download the source code of contracts using Etherscan",
    action='store_true',
)

analyzer = parser.add_argument_group(title="Analyzer options")
analyzer.add_argument(
    "--semgrep",
    help="Run static code analysis using Semgrep",
    action='store_true',
)
