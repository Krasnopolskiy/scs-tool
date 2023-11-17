from pathlib import Path

from loguru import logger
from semgrep.run_scan import run_scan_and_return_json
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from analyzers.semgrep.constants import CONFIG_PATH
from common.constants import SOURCE_PATH
from common.schemas import Address

CONFIG = Path(__file__).parent / CONFIG_PATH

async def analyze(address: Address) -> CliOutput:
    """
    The `analyze` function runs a semgrep analysis on a given address and returns the analysis report as
    a `CliOutput` object.
    
    :param address: The `address` parameter is of type `Address`. It represents the address of a
    directory where the analysis will be performed
    :type address: Address
    :return: The function `analyze` is returning an instance of the `CliOutput` class.
    """
    target = SOURCE_PATH / address
    target.mkdir(parents=True, exist_ok=True)
    logger.info("Running semgrep analysis on {}", address)
    report = run_scan_and_return_json(config=CONFIG, targets=[target], no_git_ignore=True)
    return CliOutput.from_json(report)
