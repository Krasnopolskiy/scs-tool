import re

from bs4 import BeautifulSoup

from common.schemas import Address, ContractFile

contract_file_regex = re.compile(r"File (\d+) of (\d+) : ([\w.-]+)")
address_regex = re.compile(r"/address/(\w+)")


def parse_transaction_list(html: str) -> list[Address]:
    """
    The function `parse_transaction_list` extracts addresses from an HTML document and returns them as a
    list.
    
    :param html: The `html` parameter is a string that represents the HTML content of a web page
    :type html: str
    :return: The function `parse_transaction_list` returns a list of `Address` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    addresses: list[Address] = []
    for row in soup.find("tbody").find_all("tr"):
        for tag in row.find_all("a", href=address_regex):
            addresses.extend(address_regex.match(tag["href"]).groups())
    return addresses


def parse_contract_files(html: str) -> list[ContractFile]:
    """
    The function `parse_contract_files` takes an HTML string, extracts contract file information, and
    returns a list of `ContractFile` objects.
    
    :param html: The `html` parameter is a string that represents the HTML content of a webpage
    :type html: str
    :return: The function `parse_contract_files` returns a list of `ContractFile` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    files: list[ContractFile] = []
    for tag in soup.find_all(text=contract_file_regex):
        _, _, name = contract_file_regex.match(tag.text).groups()
        content = tag.findNext("pre").text
        files.append(ContractFile(name=name, content=content))
    return files
