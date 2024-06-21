from argparse import ArgumentParser

from cli.types import address_type, transaction_type

parser = ArgumentParser(
    description="Smart Contract Security Tool",
)

loader = parser.add_argument_group(title="Address loader options")
loader.add_argument(
    "-a",
    "--addresses",
    nargs="+",
    type=address_type,
    help="List of address IDs containing the contracts to be parsed",
)
loader.add_argument(
    "-t",
    "--transactions",
    nargs="+",
    type=transaction_type,
    help="List of transactions IDs containing the contracts to be parsed",
)
loader.add_argument(
    "-l",
    "--local",
    help="Load the addresses of contracts containing in the local file system",
    action="store_true",
)

scanner = parser.add_argument_group(title="Scanner options")
scanner.add_argument(
    "--etherscan",
    help="Download the source code of contracts using Etherscan",
    action="store_true",
)

analyzer = parser.add_argument_group(title="Analyzer options")
analyzer.add_argument(
    "--decompile",
    help="Run bytecode decompilation using Panoramix",
    action="store_true",
)
analyzer.add_argument(
    "--semgrep",
    help="Run static code analysis using Semgrep",
    action="store_true",
)
analyzer.add_argument(
    "--mythril",
    help="Run static code analysis using Mythril",
    action="store_true",
)
analyzer.add_argument(
    "--slither",
    help="Run static code analysis using Slither",
    action="store_true",
)
