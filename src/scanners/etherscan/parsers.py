import re
from binascii import unhexlify

from bs4 import BeautifulSoup, Tag

from common.schemas import Address
from scanners.etherscan.schemas import ContractSourceFile, ContractByteFile

BYTECODE_HEADER = r"Deployed Bytecode"

contract_file_regex = re.compile(r"File (\d+) of (\d+) : ([\w.-]+)")
address_regex = re.compile(r"/address/(\w+)")


def parse_transaction_list(html: str) -> list[Address]:
    """
    The function `parse_transaction_list` takes an HTML string, extracts addresses from a table, and
    returns a list of addresses.

    :param html: A string containing HTML code
    :type html: str
    :return: The function `parse_transaction_list` returns a list of `Address` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    addresses: list[Address] = []
    if table := soup.find("tbody"):
        for row in table.find_all("tr"):
            for tag in row.find_all("a", href=address_regex):
                addresses.extend(address_regex.match(tag["href"]).groups())
    return addresses


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


def parse_contract_bytecode(html: str) -> list[ContractByteFile]:
    """
    The function `parse_contract_bytecode` extracts bytecode from an HTML document and returns it as a
    list of `ContractByteFile` objects.

    :param html: A string containing HTML code
    :type html: str
    :return: The function `parse_contract_bytecode` is returning a list of `ContractByteFile` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.findAll("h4", attrs={"class": "card-header-title"})
    code = soup.find(id="dividcode").findChild("pre")
    for header in headers:  # type: Tag
        if header.text == BYTECODE_HEADER:
            code = header.findNext("pre")
    bytecode = code.text.replace("0x", "")
    return [ContractByteFile(content=unhexlify(bytecode))]


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
        addresses.extend(address_regex.match(tag["href"]).groups())
    return addresses
