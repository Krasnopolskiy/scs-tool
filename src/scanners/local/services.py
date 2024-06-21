from common.constants import SOURCE_PATH
from common.schemas import Address


async def load_local_addresses() -> list[Address]:
    """
    This Python function loads local addresses from directories with names starting with "0x" and
    returns a list of Address objects.
    :return: A list of Address objects is being returned.
    """
    directories = SOURCE_PATH.glob("0x*")
    addresses = []
    for directory in directories:
        try:
            addresses.append(Address(directory.name))
        except ValueError:
            pass
    return addresses
