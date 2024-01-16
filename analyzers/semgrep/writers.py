import json

from loguru import logger
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from common.constants import SOURCE_PATH
from common.schemas import Address


def write_report_files(address: Address, output: CliOutput):
    """
    The function `write_report_files` writes a JSON report file based on the given address and decompilation.

    :param address: The `address` parameter is of type `Address` and represents the location where the
    report file will be written. It could be a directory path or a file path
    :type address: Address
    :param output: The `decompilation` parameter is of type `CliOutput`. It likely represents the decompilation of a
    command-line interface operation or a series of results
    :type output: CliOutput
    """
    report_file = SOURCE_PATH / address / "report.json"
    report = [result.to_json() for result in output.results]
    with report_file.open("w", encoding="utf-8") as out:
        out.write(json.dumps(report))
    logger.info("Writing {}", report_file)
