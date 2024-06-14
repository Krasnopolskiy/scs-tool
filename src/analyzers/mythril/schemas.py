from dataclasses import dataclass

from loguru import logger
from mythril.analysis.report import Report

from analyzers.mythril.constants import MYTHRIL_REPORT_FILE
from common.schemas import Address, BaseFile


@dataclass
class MythrilReportFile(BaseFile[Report]):
    name: str = MYTHRIL_REPORT_FILE

    def get_content(self) -> str:
        """
        The function `get_content` returns the content of an object in JSON format.
        :return: The `get_content` method is returning the content of the object in JSON format by
        calling the `as_json` method on the `content` attribute of the object.
        """
        return self.content.as_json()

    def write(self, address: Address):
        """
        The function writes address information and logs any issues related to the content.

        :param address: The `address` parameter in the `write` method is an instance of the `Address`
        class. It is used to specify the address where the content will be written
        :type address: Address
        """
        super().write(address)
        for issue in self.content.issues.values():
            logger.warning("[{}] {}:{} {}", address, issue.filename, issue.lineno, issue.description)
