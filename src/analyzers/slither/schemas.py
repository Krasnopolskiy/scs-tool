from dataclasses import dataclass

from loguru import logger
from pydantic import BaseModel

from analyzers.slither.constants import SLITHER_REPORT_FILE
from common.schemas import Address, BaseFile


class Issue(BaseModel):
    class Config:
        extra = "ignore"

    description: str


class Report(BaseModel):
    class Config:
        extra = "ignore"

    results: list[Issue]


@dataclass
class SlitherReportFile(BaseFile[Report]):
    name: str = SLITHER_REPORT_FILE

    def get_content(self) -> str:
        """
        This function returns the JSON dump of the content model.
        :return: The `get_content` method is returning the JSON dump of the model content stored in the
        `self.content` attribute.
        """
        return self.content.model_dump_json()

    def write(self, address: Address):
        """
        The function writes address information and logs any issues related to the content.

        :param address: The `address` parameter in the `write` method is an instance of the `Address`
        class. It is used to specify the address where the content is being written to or read from
        :type address: Address
        """
        super().write(address)
        for issue in self.content.results:
            logger.warning("[{}] {}", address, issue.description)
