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
