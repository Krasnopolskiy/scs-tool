from copy import deepcopy
from pathlib import Path

from loguru import logger
from slither.__main__ import choose_detectors, choose_printers, get_detectors_and_printers, process_all

from analyzers.slither.config import ARGS
from analyzers.slither.schemas import Report, SlitherReportFile
from common.constants import SOURCE_PATH
from common.schemas import Address
from common.utils import switch_solc_binary


def setup_analyzer(targets: list[Path]):
    """
    The function `setup_analyzer` takes a list of file paths, sets up the Solidity compiler binary,
    arguments, detectors, and printers, and returns them for analysis.
    
    :param targets: Targets is a list of Path objects representing the file paths to be analyzed. The
    `setup_analyzer` function takes this list of file paths as input and performs various operations on
    them, such as reading the contents of the first target, setting up arguments, getting detectors and
    printers, and returning the arguments
    :type targets: list[Path]
    :return: The function `setup_analyzer` is returning a tuple containing three elements:
    1. `args`: A modified copy of the global variable `ARGS` with the `filename` attribute set to a list
    of file paths converted to strings.
    2. `choose_detectors(args, detectors)`: The result of selecting relevant detectors based on the
    provided arguments and the available detectors.
    3. `choose_printers
    """
    switch_solc_binary(targets[0].read_text())
    args = deepcopy(ARGS)

    args.filename = [str(target) for target in targets]

    detectors, printers = get_detectors_and_printers()

    return args, choose_detectors(args, detectors), choose_printers(args, printers)


async def analyze(address: Address) -> SlitherReportFile | None:
    """
    The `analyze` function takes an `Address` object, searches for Solidity files, runs Slither analysis
    on them, and returns a `SlitherReportFile` containing the analysis results.
    
    :param address: The `address` parameter in the `analyze` function is of type `Address`. It seems
    like the function is designed to analyze Solidity files located at a specific address path. The
    function first locates all Solidity files (with a `.sol` extension) within the specified address
    path, then
    :type address: Address
    :return: The `analyze` function returns either a `SlitherReportFile` object containing the analysis
    results if there are Solidity files to analyze, or `None` if there are no Solidity files found for
    analysis.
    """
    target = SOURCE_PATH / address
    targets = list(target.rglob("*.sol"))
    if not targets:
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running slither analysis", address)

    args, detectors, printers = setup_analyzer(targets)
    _, results_detectors, _, _ = process_all(str(target), args, detectors, printers)

    return SlitherReportFile(content=Report(issues=results_detectors))
