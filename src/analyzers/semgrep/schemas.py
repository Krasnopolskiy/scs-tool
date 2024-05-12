import json
from dataclasses import dataclass

from loguru import logger
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from analyzers.semgrep.constants import SEMGREP_REPORT_FILE
from common.schemas import Address, BaseFile


@dataclass
class SemgrepReportFile(BaseFile[CliOutput]):
    name: str = SEMGREP_REPORT_FILE

    def get_content(self) -> str:
        """
        The function `get_content` returns a JSON representation of the results in the `content`
        attribute.
        :return: A JSON string representation of the results from the content attribute of the object.
        """
        report = [result.to_json() for result in self.content.results]
        return json.dumps(report)

    def write(self, address: Address):
        """
        The `write` function writes an address and logs warning messages for each result in the content.

        :param address: The `address` parameter in the `write` method is an instance of the `Address`
        class. It is used to specify the address where the content should be written to
        :type address: Address
        """
        super().write(address)
        for result in self.content.results:
            logger.warning("[{}] {}:{} {}", address, result.path.value, result.start.line, result.extra.message)
