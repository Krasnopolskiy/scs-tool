import os
from copy import deepcopy
from pathlib import Path

from loguru import logger
from mythril.interfaces.cli import load_code, set_config
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler

from analyzers.myth.config import ARGS
from analyzers.myth.schemas import MythrilReportFile
from common.constants import SOURCE_PATH
from common.schemas import Address
from solc.solc import get_solc_binary


def setup_analyzer(targets: list[Path]):
    """
    The function `setup_analyzer` sets up a Mythril analyzer for analyzing Solidity files.

    :param targets: Targets is a list of file paths that the function `setup_analyzer` will use to set
    up the analyzer. The function reads the content of the first target file to get the solc binary,
    sets the SOLC environment variable, and then initializes various components needed for the
    MythrilAnalyzer
    :type targets: list[Path]
    :return: MythrilAnalyzer(strategy=args.strategy, disassembler=disassembler, address=address,
    cmd_args=args)
    """
    solc = get_solc_binary(targets[0].read_text())
    os.environ["SOLC"] = str(solc)

    args = deepcopy(ARGS)
    args.solidity_files = [str(target) for target in targets]

    set_config(args)
    disassembler = MythrilDisassembler()
    address = load_code(disassembler, args)

    return MythrilAnalyzer(strategy=args.strategy, disassembler=disassembler, address=address, cmd_args=args)


async def analyze(address: Address) -> MythrilReportFile | None:
    """
    This Python function analyzes Solidity files at a given address using Mythril and returns a report
    file if analysis is successful.

    :param address: The `address` parameter in the `analyze` function represents the address of a smart
    contract that you want to analyze using the Mythril tool. The function first constructs a target
    path based on the provided address, searches for Solidity files in that path, sets up the Mythril
    analyzer for those files
    :type address: Address
    :return: The function `analyze` returns either a `MythrilReportFile` object containing the analysis
    report if there are Solidity files to analyze, or `None` if there are no Solidity files found for
    analysis.
    """
    target = SOURCE_PATH / address
    targets = list(target.rglob("*.sol"))
    if not targets:
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running mythril analysis", address)
    analyzer = setup_analyzer(targets)
    report = analyzer.fire_lasers(transaction_count=ARGS.transaction_count)
    return MythrilReportFile(content=report)
