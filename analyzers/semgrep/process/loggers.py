from loguru import logger
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput


def log_report(output: CliOutput):
    """
    The `log_report` function logs warning messages for each result in the given `CliOutput` object.

    :param output: The `output` parameter is an instance of the `CliOutput` class. It contains the
    results of a command line operation, such as running a script or executing a command
    :type output: CliOutput
    """
    for result in output.results:
        logger.warning("{}: {}", result.path.value, result.extra.message)
