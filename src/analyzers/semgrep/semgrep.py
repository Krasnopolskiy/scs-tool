from pathlib import Path

from loguru import logger
from semgrep.run_scan import run_scan_and_return_json
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from analyzers.semgrep.constants import CONFIG_PATH
from analyzers.semgrep.schemas import ContractReportFile
from common.config.constants import SOURCE_PATH
from common.schemas import Address

CONFIG = Path(__file__).parent / CONFIG_PATH


async def analyze(address: Address) -> ContractReportFile | None:
    target = SOURCE_PATH / address
    if not target.exists():
        logger.info("[{}] Nothing to analyze", address)
        return None
    logger.info("[{}] Running semgrep analysis", address)
    report = run_scan_and_return_json(config=CONFIG, targets=[target], no_git_ignore=True)
    return ContractReportFile(content=CliOutput.from_json(report))
