import binascii
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from loguru import logger

from common.schemas import Address
from scanners.etherscan.api.schemas import ContractSourceResponse
from scanners.etherscan.schemas import ContractByteFile, ContractSourceFile

BYTECODE_HEADER = r"Deployed Bytecode"

contract_file_regex = re.compile(r"File (\d+) of (\d+) : ([\w.-]+)")
address_regex = re.compile(r"/address/(\w+)")


def parse_contract_files(html: str) -> list[ContractSourceFile]:
    """
    The function `parse_contract_files` takes an HTML string, extracts contract file names and content,
    and returns a list of `ContractSourceFile` objects.

    :param html: The `html` parameter is a string that represents the HTML content of a webpage
    :type html: str
    :return: The function `parse_contract_files` returns a list of `ContractSourceFile` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    files: list[ContractSourceFile] = []
    for tag in soup.find_all(text=contract_file_regex):
        _, _, name = contract_file_regex.match(tag.text).groups()
        content = tag.findNext("pre").text
        files.append(ContractSourceFile(name=name, content=content))
    return files


def parse_contract_bytecode(html: str, address: Address) -> list[ContractByteFile]:
    """
    The function `parse_contract_bytecode` parses HTML to extract bytecode and returns it as a list of
    `ContractByteFile` objects.

    :param html: The `html` parameter is a string that represents the HTML content of a web page
    :type html: str
    :param address: The `address` parameter is the address of a contract. It is of type `Address`
    :type address: Address
    :return: The function `parse_contract_bytecode` returns a list of `ContractByteFile` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.findAll("h4", attrs={"class": "card-header-title"})
    code = soup.find(id="dividcode").findChild("pre")
    for header in headers:  # type: Tag
        if header.text == BYTECODE_HEADER:
            code = header.findNext("pre")
    try:
        bytecode = code.text.replace("0x", "")
        content = binascii.unhexlify(bytecode)
    except (AttributeError, binascii.Error):
        logger.warning("[{}] No bytecode found", address)
        content = b""
    return [ContractByteFile(content)]


def parse_transaction(html: str) -> list[Address]:
    """
    The function `parse_transaction` takes an HTML string as input, extracts addresses from the HTML
    using a regular expression, and returns a list of addresses.

    :param html: A string containing HTML code
    :type html: str
    :return: The function `parse_transaction` returns a list of `Address` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    addresses: list[Address] = []
    for tag in soup.find_all(href=address_regex):
        if tag.find("span"):  # Donation address
            continue
        if tag.findPrevious("i", attrs={"aria-label": "Contract"}):
            addresses.extend(address_regex.match(tag["href"]).groups())
    return addresses


def parse_contract_source_response(response: ContractSourceResponse) -> list[ContractSourceFile]:
    """
    The function `parse_contract_source_response` extracts contract source files from a response object
    containing contract data in JSON format.

    :param response: ContractSourceResponse is a data structure that contains information about
    contracts, including their source code. It likely has a property called "contracts" which is a list
    of contract objects
    :type response: ContractSourceResponse
    :return: A list of `ContractSourceFile` objects is being returned.
    """
    files: list[ContractSourceFile] = []
    for contract in response.contracts:
        if contract.data.startswith("{{"):
            data = json.loads(contract.data[1:-1])
            for name, source in data["sources"].items():
                content = source["content"]
                filename = Path(name).name
                files.append(ContractSourceFile(name=filename, content=content))
        elif contract.data.startswith("{"):
            data = json.loads(contract.data)
            for name, source in data.items():
                content = source["content"]
                filename = Path(name).name
                files.append(ContractSourceFile(name=filename, content=content))
        else:
            files.append(ContractSourceFile(name="contract.sol", content=contract.data))
    return files
