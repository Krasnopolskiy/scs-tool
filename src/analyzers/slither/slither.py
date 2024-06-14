from copy import deepcopy
from pathlib import Path

from loguru import logger
from slither.__main__ import choose_detectors, choose_printers, get_detectors_and_printers, process_all

from analyzers.slither.config import ARGS
from analyzers.slither.schemas import Report, SlitherReportFile
from common.constants import SOURCE_PATH
from common.schemas import Address
from solc.solc import get_solc_binary


def setup_analyzer(targets: list[Path]):
    """
    The function `setup_analyzer` takes a list of file paths as input, sets up the Solidity analyzer
    with the necessary arguments and detectors, and returns the configured analyzer.

    :param targets: Targets is a list of Path objects representing the file paths of Solidity source
    code files that you want to analyze. The `setup_analyzer` function takes this list of targets as
    input to set up the analyzer for those specific Solidity files
    :type targets: list[Path]
    :return: The function `setup_analyzer` returns a tuple containing three elements:
    1. `args`: A dictionary containing configuration arguments for the analyzer.
    2. A list of detector objects chosen based on the configuration arguments.
    3. A list of printer objects chosen based on the configuration arguments.
    """
    solc = get_solc_binary(targets[0].read_text())
    args = deepcopy(ARGS)

    args.filename = [str(target) for target in targets]
    args.solc = str(solc)

    detectors, printers = get_detectors_and_printers()

    return args, choose_detectors(args, detectors), choose_printers(args, printers)


async def analyze(address: Address):
    """
    The function `analyze` takes an `Address` object, locates Solidity files at the specified address,
    runs Slither analysis on them, and returns a `SlitherReportFile` containing the analysis results.

    :param address: The `address` parameter in the `analyze` function seems to represent the address of
    a directory where Solidity files are located. The function then searches for Solidity files within
    that directory, runs Slither analysis on those files, and returns a `SlitherReportFile` containing
    the analysis results
    :type address: Address
    :return: The function `analyze` is returning a `SlitherReportFile` object with the content being a
    `Report` object containing the results of the Slither analysis performed on the Solidity files found
    at the specified address.
    """
    target = SOURCE_PATH / address
    targets = list(target.rglob("*.sol"))
    if not targets:
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running slither analysis", address)

    args, detectors, printers = setup_analyzer(targets)
    _, results_detectors, _, _ = process_all(str(target), args, detectors, printers)

    return SlitherReportFile(content=Report(results=results_detectors))
