import json
from copy import deepcopy
from pathlib import Path

from loguru import logger
from mythril.interfaces.cli import load_code, set_config
from mythril.mythril import MythrilAnalyzer, MythrilDisassembler

from analyzers.mythril.config import ARGS
from analyzers.mythril.schemas import MythrilReportFile, Report
from common.constants import SOURCE_PATH
from common.schemas import Address
from common.utils import switch_solc_binary


def setup_analyzer(targets: list[Path]):
    """
    The `setup_analyzer` function initializes a MythrilAnalyzer with specified targets and configuration
    settings.
    
    :param targets: A list of file paths to Solidity files that will be analyzed
    :type targets: list[Path]
    :return: MythrilAnalyzer(strategy=args.strategy, disassembler=disassembler, address=address,
    cmd_args=args)
    """
    switch_solc_binary(targets[0].read_text())

    args = deepcopy(ARGS)
    args.solidity_files = [str(target) for target in targets]

    set_config(args)
    disassembler = MythrilDisassembler()
    address = load_code(disassembler, args)

    return MythrilAnalyzer(strategy=args.strategy, disassembler=disassembler, address=address, cmd_args=args)


async def analyze(address: Address) -> MythrilReportFile | None:
    """
    This Python function analyzes Solidity smart contracts using Mythril and returns a Mythril report
    file if contracts are found for analysis.
    
    :param address: The `address` parameter in the `analyze` function represents the address of a smart
    contract that you want to analyze using Mythril
    :type address: Address
    :return: The `analyze` function returns either a `MythrilReportFile` object or `None`.
    """
    target = SOURCE_PATH / address
    targets = list(target.rglob("*.sol"))
    if not targets:
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running mythril analysis", address)
    analyzer = setup_analyzer(targets)
    report = analyzer.fire_lasers(transaction_count=ARGS.transaction_count)
    report = json.loads(report.as_json())
    return MythrilReportFile(content=Report(**report))
