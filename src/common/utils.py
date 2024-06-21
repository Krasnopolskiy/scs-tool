import re

from loguru import logger
from solc_select.solc_select import switch_global_version

NOTHING = object()

VERSION = re.compile(r"pragma solidity .*(\d\.\d\.\d).*")


def handle_exceptions(default=NOTHING):
    """
    The `handle_exceptions` decorator in Python catches exceptions raised by the decorated async
    function and logs them, optionally returning a default value.

    :param default: The `default` parameter in the `handle_exceptions` decorator function is used to
    specify a default value that will be returned if an exception occurs within the decorated function.
    If no `default` value is provided, the decorator will not return anything in case of an exception
    :return: The `handle_exceptions` function is a decorator that catches exceptions raised by the
    decorated function. If an exception is caught, it logs the error and returns the `default` value if
    provided. If no `default` value is provided, it returns `NOTHING`.
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except (Exception, BaseException) as exc:
                logger.error(exc)
                if default is not NOTHING:
                    return default

        return wrapper

    return decorator


def switch_solc_binary(contract: str):
    """
    The function `switch_solc_binary` extracts the version of a contract, and then switches the global
    version to that extracted version.

    :param contract: The `switch_solc_binary` function takes a `contract` parameter, which is expected
    to be a string representing a Solidity smart contract. The function attempts to extract the version
    of the Solidity compiler used in the contract using a regular expression pattern stored in
    `VERSION`. If the version is successfully
    :type contract: str
    """
    try:
        version = VERSION.search(contract).group(1)
        switch_global_version(version, always_install=True)
    except Exception as exc:
        logger.error(exc)
