from pydantic import TypeAdapter

from common.schemas import Address, Transaction


def address_type(arg: str) -> Address:
    """
    The function `address_type` takes a string argument, validates it using a TypeAdapter, and returns
    an instance of the Address class.

    :param arg: arg is a string that represents an address
    :type arg: str
    :return: an instance of the `Address` class.
    """
    adapter = TypeAdapter(Address)
    adapter.validate_python(arg)
    return Address(arg)


def transaction_type(arg: str) -> Transaction:
    """
    The function `transaction_type` takes a string argument, validates it using a TypeAdapter, and
    returns a Transaction object.
    
    :param arg: The parameter `arg` is a string that represents the transaction type
    :type arg: str
    :return: an instance of the `Transaction` class.
    """
    adapter = TypeAdapter(Transaction)
    adapter.validate_python(arg)
    return Transaction(arg)


def transactions_number_type(arg: str) -> int:
    """
    The function `transactions_number_type` takes a string argument and converts it to an integer,
    raising a ValueError if the integer is greater than 100,000 or less than 0.

    :param arg: The parameter `arg` is a string that represents the size of transactions
    :type arg: str
    :return: the size of the transactions, which is an integer.
    """
    size = int(arg)
    if size > 100_000 or size < 0:
        raise ValueError
    return size
