import re
from pathlib import Path

VERSION = re.compile(r"pragma solidity .+(\d\.\d\.\d).+")

BASE_PATH = Path(__file__).parent

SOLC_BINARIES = {
    "0.4": BASE_PATH / "solc-0.4.25",
    "0.5": BASE_PATH / "solc-0.5.17",
    "0.6": BASE_PATH / "solc-0.6.12",
    "0.7": BASE_PATH / "solc-0.7.6",
    "0.8": BASE_PATH / "solc-0.8.26",
}


def get_solc_binary(contract: str) -> Path | None:
    """
    This Python function retrieves the Solidity compiler binary based on the version extracted from a
    contract string.

    :param contract: The `contract` parameter is expected to be a string representing the contract code.
    The function attempts to extract the version number from this contract code using a regular
    expression pattern stored in `VERSION`. If the version number is successfully extracted, it then
    splits the version number into major, minor, and patch components
    :type contract: str
    :return: The function `get_solc_binary` returns either a `Path` object or `None`.
    """
    try:
        version = VERSION.search(contract).group(1)
    except AttributeError:
        return None
    major, minor, _ = version.split(".")
    return SOLC_BINARIES.get(f"{major}.{minor}")
