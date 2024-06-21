from pathlib import Path

from loguru import logger
from semgrep.run_scan import run_scan_and_return_json

from analyzers.semgrep.constants import CONFIG_PATH
from analyzers.semgrep.schemas import Report, SemgrepReportFile
from common.constants import SOURCE_PATH
from common.schemas import Address

CONFIG = Path(__file__).parent / CONFIG_PATH


async def analyze(address: Address) -> SemgrepReportFile | None:
    """
    This Python function analyzes a given address using Semgrep and returns a Semgrep report file if the
    target exists.

    :param address: The `address` parameter in the `analyze` function represents the location of the
    code that you want to analyze using Semgrep. It is used to specify the target directory or file path
    where the code is located
    :type address: Address
    :return: The `analyze` function returns either a `SemgrepReportFile` object or `None`.
    """
    target = SOURCE_PATH / address
    if not target.exists():
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running semgrep analysis", address)
    report = run_scan_and_return_json(config=CONFIG, targets=[target], no_git_ignore=True)
    return SemgrepReportFile(content=Report(**report))
