import json
from dataclasses import dataclass

from loguru import logger
from semgrep.semgrep_interfaces.semgrep_output_v1 import CliOutput

from analyzers.semgrep.constants import REPORT_FILE
from common.schemas import BaseFile, Address


@dataclass
class ContractReportFile(BaseFile[CliOutput]):
    name: str = REPORT_FILE

    def get_content(self) -> str:
        report = [result.to_json() for result in self.content.results]
        return json.dumps(report)

    def write(self, address: Address):
        super().write(address)
        for result in self.content.results:
            logger.warning("[{}] {}:{} {}", address, result.path.value, result.start.line, result.extra.message)
