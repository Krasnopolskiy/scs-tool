import re
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup
from loguru import logger

BASE_PATH = "sources/"
source_file_regex = re.compile(r"File (\d+) of (\d+) : ([\w.-]+)")


@dataclass
class SourceFile:
    name: str
    source: str


def parse_contract_files(html: str) -> list[SourceFile]:
    """
    The function `parse_contract_files` takes an HTML string, extracts source file information using
    regular expressions, and returns a list of `SourceFile` objects containing the file name and source
    code.

    :param html: A string containing HTML code
    :type html: str
    :return: The function `parse_contract_files` returns a list of `SourceFile` objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    files: list[SourceFile] = []
    for tag in soup.find_all(text=source_file_regex):
        _, _, name = source_file_regex.match(tag.text).groups()
        source = tag.findNext("pre").text
        files.append(SourceFile(name=name, source=source))
    return files


async def save_contract_files(transaction_id: str, html: str):
    """
    The function `save_contract_files` saves contract files to a specified directory based on the
    transaction ID.

    :param transaction_id: A unique identifier for the transaction. It is used to create a directory to
    save the contract files
    :type transaction_id: str
    :param html: The `html` parameter is a string that represents the HTML content of a webpage
    :type html: str
    """
    source_files = parse_contract_files(html)
    logger.info("Transaction {} contains {} files", transaction_id, len(source_files))
    if not source_files:
        return
    directory = BASE_PATH + transaction_id
    Path(directory).mkdir(parents=True, exist_ok=True)
    for file in source_files:
        with open(f"{directory}/{file.name}", "w", encoding="utf-8") as out:
            out.write(file.source)
    logger.info("Transaction {} source files saved to the {}", transaction_id, directory)
