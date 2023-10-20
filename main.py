import asyncio
import re
from argparse import ArgumentParser, ArgumentTypeError

from etherscan.client import fetch_contract_html
from etherscan.parser import save_contract_files

transaction_id_regex = re.compile(r"^0x[a-fA-F0-9]{40}$")


def transaction_id_type(arg_value: str, regex: re.Pattern = transaction_id_regex) -> str:
    """
    The function `transaction_id_type` checks if a given string matches a specific regex pattern and
    returns the string if it does, otherwise it raises an error.

    :param arg_value: The `arg_value` parameter is a string that represents the transaction ID
    :type arg_value: str
    :param regex: The `regex` parameter is a regular expression pattern object that is used to validate
    the `arg_value` parameter. It is expected to be an instance of the `re.Pattern` class from the `re`
    module
    :type regex: re.Pattern
    :return: the argument value if it matches the specified regular expression pattern.
    """
    if not regex.match(arg_value):
        raise ArgumentTypeError("Invalid transaction ID. Format: 0x[a-fA-F0-9]{40}")
    return arg_value.lower()


async def process_transaction(transaction):
    """
    The function "process_transaction" fetches the HTML of a contract and saves it as files.

    :param transaction: The `transaction` parameter is an object that represents a transaction. It
    likely contains information such as the transaction ID, sender, recipient, amount, and any other
    relevant details related to the transaction
    """
    html = await fetch_contract_html(transaction)
    await save_contract_files(transaction, html)


async def main(transactions: list[str]):
    """
    The `main` function asynchronously processes a list of transactions using the `process_transaction`
    function.

    :param transactions: The `transactions` parameter is a list of strings. Each string represents a
    transaction that needs to be processed
    :type transactions: list[str]
    """
    tasks = []
    for transaction in transactions:
        task = asyncio.ensure_future(process_transaction(transaction))
        tasks.append(task)
    await asyncio.gather(*tasks)


parser = ArgumentParser(
    description="Blockchain Contract Parser",
)
parser.add_argument(
    "transactions",
    type=transaction_id_type,
    help="List of transaction IDs containing the contracts to be parsed",
    nargs="+",
)

if __name__ == "__main__":
    transactions = parser.parse_args().transactions
    asyncio.run(main(transactions))
