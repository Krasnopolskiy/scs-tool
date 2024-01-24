import json

from loguru import logger
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from analyzers.semgrep.constants import REPORT_FILE
from common.constants import SOURCE_PATH
from common.schemas import Address


def write_report_files(address: Address, output: CliOutput):
    """
    The function `write_report_files` writes a JSON report file containing the results of a CLI output
    to a specified address.

    :param address: The `address` parameter is of type `Address` and represents the location where the
    report files will be written. It could be a directory path or any other address format that is
    compatible with the file system
    :type address: Address
    :param output: The `output` parameter is of type `CliOutput`. It likely contains the results of some
    command-line operation or process
    :type output: CliOutput
    """
    target = SOURCE_PATH / address / REPORT_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    report = [result.to_json() for result in output.results]
    with target.open("w", encoding="utf-8") as out:
        out.write(json.dumps(report))
    logger.info("Writing {}", target)
